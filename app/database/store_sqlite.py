# app/database/store_sqlite.py
import sqlite3
import os

DB_FILE = "code_base.db"

class SQLiteStore:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Створення таблиць
        c.execute('CREATE TABLE IF NOT EXISTS languages (id INTEGER PRIMARY KEY, name TEXT UNIQUE, file_count INTEGER)')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY, 
            language_id INTEGER, 
            path TEXT, 
            name TEXT, 
            relpath TEXT, 
            size INTEGER, 
            lines INTEGER, 
            mtime REAL,
            FOREIGN KEY(language_id) REFERENCES languages(id))
        ''')
        
        # Індекси
        c.execute('CREATE INDEX IF NOT EXISTS idx_name ON files(name)')
        conn.commit()
        conn.close()

    def save_scan_result(self, data):
        if not data or 'languages' not in data: return

        conn = sqlite3.connect(self.db_path)
        # ОПТИМІЗАЦІЯ: Вимикаємо безпечні перевірки на час масового запису
        conn.execute("PRAGMA synchronous = OFF")
        conn.execute("PRAGMA journal_mode = MEMORY")
        
        c = conn.cursor()
        
        print("💾 Очищення старої бази...")
        c.execute('DELETE FROM files')
        c.execute('DELETE FROM languages')
        
        print("💾 Запис нових даних...")
        
        # Використовуємо одну велику транзакцію
        try:
            for lang, info in data['languages'].items():
                c.execute('INSERT INTO languages (name, file_count) VALUES (?, ?)', (lang, info['count']))
                lang_id = c.lastrowid
                
                # Масова вставка файлів (bulk insert)
                files_data = []
                for f in info['files']:
                    files_data.append((
                        lang_id, f['path'], f['name'], f['relpath'], f['size'], f['lines'], f['mtime']
                    ))
                
                # Записуємо пакетами
                if files_data:
                    c.executemany('''
                        INSERT INTO files (language_id, path, name, relpath, size, lines, mtime) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', files_data)
            
            conn.commit() # Фіксуємо зміни
            print("✅ База даних успішно збережена!")
            
        except Exception as e:
            print(f"❌ Помилка запису в БД: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(lines) FROM files")
        res = c.fetchone()
        conn.close()
        return res if res and res[0] else (0, 0)

    # Метод для GUI (дерево файлів)
    def get_tree_data(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        tree = {}
        c.execute("SELECT id, name FROM languages ORDER BY name")
        langs = c.fetchall()
        
        for lang_id, lang_name in langs:
            # Обмежуємо вивід у дереві до 500 файлів на мову, щоб GUI не гальмував
            c.execute("SELECT name, lines, size, path FROM files WHERE language_id=? ORDER BY lines DESC LIMIT 500", (lang_id,))
            files = c.fetchall()
            if files:
                tree[lang_name] = files
                
        conn.close()
        return tree