# app/core/search.py
import sqlite3
import os

class SearchEngine:
    def __init__(self, db_path="code_base.db"):
        self.db_path = db_path

    def get_languages(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM languages ORDER BY name")
            langs = [row[0] for row in cursor.fetchall()]
            conn.close()
            return langs
        except: return []

    def search_files(self, query, lang_filter=None, sort_by="size"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = """
            SELECT f.name, f.path, f.size, f.lines 
            FROM files f 
            JOIN languages l ON f.language_id = l.id
            WHERE 1=1
        """
        params = []

        # 1. Пошук за назвою (тільки якщо щось ввели)
        if query and query.strip():
            sql += " AND f.name LIKE ?"
            params.append(f'%{query}%')

        # 2. Фільтр по мові
        if lang_filter and lang_filter != "Всі мови":
            sql += " AND l.name = ?"
            params.append(lang_filter)

        # 3. Сортування
        if sort_by == "lines":
            sql += " ORDER BY f.lines DESC"
        elif sort_by == "name":
            sql += " ORDER BY f.name ASC"
        else:
            sql += " ORDER BY f.size DESC"

        sql += " LIMIT 500"
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        return results

    def search_code(self, query, lang_filter=None, limit=50):
       # Пошук тексту всередині файлів.
        if not query or len(query.strip()) < 3: 
            return []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ФОРМУЄ СПИСОК ФАЙЛІВ ДЛЯ СКАНУВАННЯ
        sql = "SELECT f.path, f.name FROM files f JOIN languages l ON f.language_id = l.id WHERE 1=1"
        params = []
        
        # Якщо обрана мова, шукаємо ТІЛЬКИ в ній
        if lang_filter and lang_filter != "Всі мови":
            sql += " AND l.name = ?"
            params.append(lang_filter)
        
        # Сортуємо: спочатку новіші або менші файли (щоб швидше знайти код користувача)
        # Але оскільки mtime може бути 0, просто беремо всі.
        # Обмежую кількість файлів для сканування (наприклад, 2000), щоб не зависло
        sql += " LIMIT 2000"
        
        cursor.execute(sql, params)
        files = cursor.fetchall()
        conn.close()

        matches = []
        count = 0
        
        print(f"🔍 CODE SEARCH: Scanning {len(files)} files for '{query}'...")

        for path, name in files:
            if count >= limit: break
            if not os.path.exists(path): continue
            
            try:
                # Відкриваємо файл (безпечно)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        # Не читає занадто далеко (перші 3000 рядків)
                        if i > 3000: break
                        
                        if query.lower() in line.lower():
                            matches.append({
                                "file": name,
                                "path": path,
                                "line": i + 1,
                                "content": line.strip()[:120]
                            })
                            count += 1
                            if count >= limit: break
            except:
                continue
                
        return matches