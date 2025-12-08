# app/utils/report.py
import os
import datetime
import webbrowser

class ReportGenerator:
    def __init__(self, db_path="code_base.db"):
        pass # Тут можна підключитись до БД, якщо треба

    def generate_html(self, stats_data, output_file="report.html"):
        """
        Генерує HTML звіт.
        stats_data = { 'total_files': 100, 'total_lines': 5000, 'languages': [...] }
        """
        
        # Формуємо рядки таблиці
        rows = ""
        for lang, count in stats_data['languages']:
            rows += f"<tr><td>{lang}</td><td>{count}</td></tr>"

        html_content = f"""
        <html>
        <head>
            <title>Звіт аналізу коду</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #f4f7f6; padding: 40px; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 800px; margin: auto; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                .stat-box {{ display: flex; gap: 20px; margin: 20px 0; }}
                .card {{ flex: 1; background: #ecf0f1; padding: 20px; border-radius: 8px; text-align: center; }}
                .num {{ font-size: 32px; font-weight: bold; color: #2980b9; display: block; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Звіт про аналіз репозиторію</h1>
                <p>Дата генерації: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
                
                <div class="stat-box">
                    <div class="card">
                        <span class="num">{stats_data['total_files']}</span>
                        Файлів проаналізовано
                    </div>
                    <div class="card">
                        <span class="num">{stats_data['total_lines']:,}</span>
                        Рядків коду
                    </div>
                </div>

                <h2>Розподіл по мовах</h2>
                <table>
                    <tr><th>Мова</th><th>Кількість файлів</th></tr>
                    {rows}
                </table>
                
                <p><i>Звіт згенеровано автоматично системою Code Analyzer Pro.</i></p>
            </div>
        </body>
        </html>
        """
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"✅ Звіт збережено: {os.path.abspath(output_file)}")
        webbrowser.open(os.path.abspath(output_file)) # Відкрити в браузері