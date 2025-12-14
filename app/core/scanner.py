# app/core/scanner.py
import os
import time
from pathlib import Path
from app.utils.consts import EXTENSIONS_MAP, IGNORE_DIRS

class Scanner:
    def __init__(self, root_path):
        self.root_path = Path(root_path)

    def scan(self, options, progress_callback=None):
        data = {
            "root": str(self.root_path),
            "generated": time.time(),
            "languages": {}
        }

        min_bytes = options.get('min_size_kb', 0) * 1024
        target_langs = set(options.get('languages', []))

        if not self.root_path.exists():
            return data

        print(f"🚀 SCAN START: {self.root_path}")
        print(f"⚙️ Config: Min {options.get('min_size_kb')}KB, Langs: {len(target_langs)}")
        
        count = 0
        
        for root, dirs, files in os.walk(str(self.root_path)):
            # Фільтрує системні папки
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            
            for file in files:
                _, ext = os.path.splitext(file)
                lang = EXTENSIONS_MAP.get(ext.lower())
                
                # Перевірка мови
                if not lang: continue
                if target_langs and lang not in target_langs: continue

                full_path = os.path.join(root, file)
                
                try:
                    size = os.path.getsize(full_path)
                    
                    if size < min_bytes: continue
                    if size > 100 * 1024 * 1024: continue

                    lines = 0
                    if size < 10 * 1024 * 1024: # Для файлів < 10MB
                        try:
                            with open(full_path, 'rb') as f:
                                buf_gen = iter(lambda: f.read(128*1024), b'')
                                lines = sum(buf.count(b'\n') for buf in buf_gen)
                        except: pass
                    else:
                        lines = size // 60

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
                    if progress_callback and count % 20 == 0:
                        progress_callback(count)

                except Exception:
                    continue

        return data