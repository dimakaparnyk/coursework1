# app/utils/api.py
import requests

class WikiClient:
    def __init__(self):
        self.base_url = "https://uk.wikipedia.org/api/rest_v1/page/summary/"
        self.mapping = {
            "Python": "Python", "C++": "C%2B%2B", "C#": "C_Sharp",
            "Java": "Java", "JavaScript": "JavaScript", "TypeScript": "TypeScript",
            "PHP": "PHP", "Go": "Go_(мова_програмування)", "HTML": "HTML", "CSS": "CSS", "SQL": "SQL"
        }

    def get_info(self, lang_name):
        slug = self.mapping.get(lang_name)
        if not slug: return None
        try:
            resp = requests.get(f"{self.base_url}{slug}", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "summary": data.get("extract", "Опис недоступний."),
                    "image": data.get("thumbnail", {}).get("source", None)
                }
        except: pass
        return None