# app/core/scanner.py
import os
import time
from pathlib import Path
from app.utils.consts import EXTENSIONS_MAP, IGNORE_DIRS

class Scanner:
    def __init__(self, root_path):
        self.root_path = Path(root_path)

    # ОСЬ ТУТ БУЛА ПОМИЛКА - ТЕПЕР МИ ПРИЙМАЄМО progress_callback
    def scan(self, progress_callback=None):
        data = {
            "root": str(self.root_path),
            "generated": time.time(),
            "languages": {}
        }

        if not self.root_path.exists():
            return data

        print(f"🚀 SMART SCAN: {self.root_path}")
        
        count = 0
        
        # Використовуємо os.walk, бо це найнадійніший спосіб фільтрувати папки
        for root, dirs, files in os.walk(str(self.root_path)):
            # Фільтруємо системні папки (щоб не було 40 000 файлів)
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            
            for file in files:
                _, ext = os.path.splitext(file)
                lang = EXTENSIONS_MAP.get(ext.lower())
                if not lang: continue

                full_path = os.path.join(root, file)
                
                try:
                    size = os.path.getsize(full_path)
                    # Пропускаємо пусті та занадто великі файли
                    if size < 50 or size > 50 * 1024 * 1024: continue

                    lines = 0
                    if size < 5 * 1024 * 1024: 
                        try:
                            with open(full_path, 'rb') as f:
                                buf_gen = iter(lambda: f.read(128*1024), b'')
                                lines = sum(buf.count(b'\n') for buf in buf_gen)
                        except: pass

                    if lang not in data['languages']:
                        data['languages'][lang] = {"count": 0, "files": [], "stats": {"extensions": {}}}
                    
                    data['languages'][lang]["files"].append({
                        "path": full_path,
                        "name": file,
                        "relpath": os.path.relpath(full_path, str(self.root_path)),
                        "size": size,
                        "lines": lines,
                        "mtime": 0
                    })
                    data['languages'][lang]["count"] += 1
                    
                    count += 1
                    
                    # Оновлюємо прогрес кожні 100 файлів
                    if progress_callback and count % 100 == 0:
                        progress_callback(count)

                except Exception:
                    continue

        return data