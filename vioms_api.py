import requests
import json

class VIOMS_News:
    def __init__(self) -> None:
        self.channels = set()
        self.news = dict()

    def check_news(self):
        for channel_id in self.channels:
            url = f"https://www.vioms.ru/api/mobile/v2/email_lists/{channel_id}/mailings.json?page=1"
            try:
                r = requests.get(url, timeout=4)
            except requests.exceptions.RequestException:
                return {"error": f"Connection error. URL: {url}"}
            try:
                news = json.loads(r.text)["mailings"]
            except json.JSONDecodeError or KeyError:
                return {"error": f"Not valid responce from URL: {url}."}

            news.sort(key=(lambda i : int(i['id'])), reverse=True)
            self.news[channel_id] = news
    
    def add_vioms_channel(self, vioms_channel_id: int = 0):
        if not vioms_channel_id:
            # read channels from db
            pass
        else:
            self.channels.add(vioms_channel_id)

news = VIOMS_News()
news.add_vioms_channel(151)
news.add_vioms_channel(163)
news.check_news()
print(json.dumps(news.news))

