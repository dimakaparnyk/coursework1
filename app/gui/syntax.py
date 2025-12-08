# app/gui/syntax.py
import html

# Спробуємо імпортувати бібліотеку. Якщо її немає - не ламаємо програму.
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_for_filename, TextLexer
    from pygments.formatters import HtmlFormatter
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False

def highlight_code(code, filename, dark_mode=True):
    """Повертає HTML. Якщо є помилка - повертає просто текст."""
    if not HAS_PYGMENTS:
        # Якщо бібліотеки немає, просто повертаємо безпечний текст
        return f"<pre style='color: {'#ccc' if dark_mode else '#000'};'>{html.escape(code)}</pre>"

    try:
        try:
            lexer = get_lexer_for_filename(filename)
        except:
            lexer = TextLexer()
        
        # Вибираємо стиль залежно від теми
        style_name = 'monokai' if dark_mode else 'colorful'
        
        formatter = HtmlFormatter(style=style_name, noclasses=True)
        html_content = highlight(code, lexer, formatter)
        
        bg_color = "#2b2b2b" if dark_mode else "#ffffff"
        text_color = "#f8f8f2" if dark_mode else "#000000"
        
        return f"<div style='background-color: {bg_color}; color: {text_color}; padding: 10px;'>{html_content}</div>"
        
    except Exception as e:
        print(f"Syntax highlight error: {e}")
        return f"<pre>{html.escape(code)}</pre>"