# app/core/search.py
import sqlite3
import os

class SearchEngine:
    def __init__(self, db_path="code_base.db"):
        self.db_path = db_path

    def search_files(self, query):
        """Шукає файли за назвою (дуже швидко, через SQL)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SQL LIKE пошук
        cursor.execute("""
            SELECT name, path, size, lines 
            FROM files 
            WHERE name LIKE ? 
            ORDER BY size DESC 
            LIMIT 50
        """, (f'%{query}%',))
        
        results = cursor.fetchall()
        conn.close()
        return results

    def search_code(self, query, limit=20):
        """Шукає текст всередині файлів (повільніше, але потужно)"""
        # Спочатку беремо список потенційно цікавих файлів (наприклад, top 500 найбільших або всіх)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT path, name FROM files ORDER BY lines DESC LIMIT 500") 
        files = cursor.fetchall()
        conn.close()

        matches = []
        count = 0
        
        for path, name in files:
            if count >= limit: break
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        if query.lower() in line.lower():
                            # Знайшли!
                            matches.append({
                                "file": name,
                                "path": path,
                                "line": i + 1,
                                "content": line.strip()
                            })
                            count += 1
                            if count >= limit: break
            except:
                continue
                
        return matches