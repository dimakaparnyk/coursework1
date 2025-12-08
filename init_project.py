import os

structure = [
    "app",
    "app/core",
    "app/database",
    "app/gui",
    "app/analysis",
    "app/utils",
    "app/resources",
    "repository",  # Сюди кидатимеш коди для аналізу
]

files = [
    "app/__init__.py",
    "app/core/__init__.py",
    "app/database/__init__.py",
    "app/gui/__init__.py",
    "app/analysis/__init__.py",
    "app/utils/__init__.py",
    "main.py",
    "requirements.txt",
    "README.md"
]

def create_structure():
    # Створення папок
    for folder in structure:
        os.makedirs(folder, exist_ok=True)
        print(f"📂 Created: {folder}")
    
    # Створення пустих файлів
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f: pass
            print(f"📄 Created: {file}")

    # Заповнення requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("PyQt5>=5.15\nmatplotlib\n")

if __name__ == "__main__":
    create_structure()