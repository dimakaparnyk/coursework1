import sqlite3
import os

DB_FILE = "code_base.db"

class SQLiteStore:
    """
    Клас для керування базою даних SQLite.
    Зберігає інформацію про проскановані файли та мови.
    """
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Ініціалізація структури БД (створення таблиць)."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Таблиця мов
        c.execute('''
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER PRIMARY KEY, 
                name TEXT UNIQUE, 
                file_count INTEGER
            )
        ''')
        
        # Таблиця файлів
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
                FOREIGN KEY(language_id) REFERENCES languages(id)
            )
        ''')
        
        # Індекс для швидкого пошуку по імені
        c.execute('CREATE INDEX IF NOT EXISTS idx_name ON files(name)')
        conn.commit()
        conn.close()

    def save_scan_result(self, data):
        """Зберігає результати сканування в БД."""
        if not data or 'languages' not in data: return
        
        conn = sqlite3.connect(self.db_path)
        # Оптимізація швидкості запису
        conn.execute("PRAGMA synchronous = OFF")
        conn.execute("PRAGMA journal_mode = MEMORY")
        c = conn.cursor()
        
        # Очищення старих даних
        c.execute('DELETE FROM files')
        c.execute('DELETE FROM languages')
        
        try:
            for lang, info in data['languages'].items():
                c.execute('INSERT INTO languages (name, file_count) VALUES (?, ?)', (lang, info['count']))
                lang_id = c.lastrowid
                
                # Підготовка batch-insert
                files_data = [
                    (lang_id, f['path'], f['name'], f['relpath'], f['size'], f['lines'], f['mtime']) 
                    for f in info['files']
                ]
                
                if files_data:
                    c.executemany('''
                        INSERT INTO files (language_id, path, name, relpath, size, lines, mtime) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', files_data)
            
            conn.commit()
        except Exception as e:
            print(f"DB Error: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_tree_data(self, limit=500):
        """Отримує дані для відображення в дереві файлів (з лімітом)."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        tree = {}
        
        c.execute("SELECT id, name FROM languages ORDER BY name")
        langs = c.fetchall()
        
        for lang_id, lang_name in langs:
            c.execute("SELECT name, lines, size, path FROM files WHERE language_id=? ORDER BY lines DESC LIMIT ?", (lang_id, limit))
            files = c.fetchall()
            if files: 
                tree[lang_name] = files
        
        conn.close()
        return tree