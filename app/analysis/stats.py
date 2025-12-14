import sqlite3

class Analytics:
    def __init__(self, db_path="code_base.db"):
        self.db_path = db_path

    def get_language_distribution(self):
        """Повертає дані для кругової діаграми"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, file_count FROM languages WHERE file_count > 0 ORDER BY file_count DESC")
        data = cursor.fetchall()
        
        conn.close()
        return data

    def get_top_large_files(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, lines, size, path FROM files ORDER BY lines DESC LIMIT ?", (limit,))
        data = cursor.fetchall()
        
        conn.close()
        return data