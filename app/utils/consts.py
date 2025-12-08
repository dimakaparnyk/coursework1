# app/utils/consts.py

# 1. Розширення файлів
EXTENSIONS_MAP = {
    '.py': 'Python', '.pyw': 'Python',
    '.c': 'C', '.h': 'C',
    '.cpp': 'C++', '.hpp': 'C++', '.cc': 'C++',
    '.cs': 'C#',
    '.java': 'Java',
    '.js': 'JavaScript', '.jsx': 'JavaScript',
    '.ts': 'TypeScript', '.tsx': 'TypeScript',
    '.php': 'PHP',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.rs': 'Rust',
    '.html': 'HTML', '.css': 'CSS', '.sql': 'SQL', '.json': 'JSON', '.xml': 'XML'
}

# 2. Папки для ігнорування (Щоб не було 40000 файлів)
IGNORE_DIRS = {
    '.git', '.svn', '.hg', '.vs', '.idea', '.vscode',
    '__pycache__', 'venv', '.venv', 'env', 'Lib', 'Scripts', 'site-packages',
    'node_modules', 'bower_components',
    'build', 'dist', 'target', 'bin', 'obj', 'debug', 'release',
    'tmp', 'temp', 'logs', 'coverage'
}

# 3. Енциклопедія мов (ЦЬОГО НЕ ВИСТАЧАЛО)
LANGUAGE_META = {
    "Python": {
        "year": 1991, "author": "Guido van Rossum",
        "paradigm": "Multi-paradigm", "typing": "Dynamic",
        "usage": "AI, Backend, Scripting", "hello_world": "print('Hello')"
    },
    "C++": {
        "year": 1985, "author": "Bjarne Stroustrup",
        "paradigm": "Multi-paradigm", "typing": "Static",
        "usage": "Games, Systems", "hello_world": "std::cout << 'Hi';"
    },
    "Java": {
        "year": 1995, "author": "James Gosling",
        "paradigm": "OOP", "typing": "Static",
        "usage": "Enterprise, Android", "hello_world": "System.out.println('Hi');"
    },
    "JavaScript": {
        "year": 1995, "author": "Brendan Eich",
        "paradigm": "Event-driven", "typing": "Dynamic",
        "usage": "Web Frontend", "hello_world": "console.log('Hi')"
    },
    "TypeScript": {
        "year": 2012, "author": "Microsoft",
        "paradigm": "OOP, Functional", "typing": "Static",
        "usage": "Large Web Apps", "hello_world": "console.log('Hi')"
    },
    "C#": {
        "year": 2000, "author": "Microsoft",
        "paradigm": "OOP", "typing": "Static",
        "usage": "Windows, Unity", "hello_world": "Console.WriteLine('Hi');"
    },
    "Go": {
        "year": 2009, "author": "Google",
        "paradigm": "Concurrent", "typing": "Static",
        "usage": "Cloud, Microservices", "hello_world": "fmt.Println('Hi')"
    },
    "PHP": {
        "year": 1995, "author": "Rasmus Lerdorf",
        "paradigm": "Imperative", "typing": "Dynamic",
        "usage": "Web Backend", "hello_world": "echo 'Hi';"
    },
    "HTML": {"year": 1993, "author": "Tim Berners-Lee", "paradigm": "Markup", "typing": "-", "usage": "Web", "hello_world": "<h1>Hi</h1>"},
    "CSS": {"year": 1996, "author": "Håkon Wium Lie", "paradigm": "Style Sheet", "typing": "-", "usage": "Web Styling", "hello_world": "body { color: red; }"},
    "SQL": {"year": 1974, "author": "IBM", "paradigm": "Declarative", "typing": "Static", "usage": "Databases", "hello_world": "SELECT * FROM table;"},
    "C": {"year": 1972, "author": "Dennis Ritchie", "paradigm": "Procedural", "typing": "Static", "usage": "OS, Embedded", "hello_world": "printf('Hi');"}
}