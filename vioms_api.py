import requests
import json

class VIOMS_News:
    def __init__(self) -> None:
        self.channels = set()
        self.news = []

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
            self.news.append([(channel_id, n) for n in news])
    
    def add_vioms_channel(self, vioms_channel_id: int = 0):
        if not vioms_channel_id:
            # TODO read channels from db
            pass
        else:
            self.channels.add(vioms_channel_id)

    def get_news_item(self, news_id: int):
        url = f"https://www.vioms.ru/api/mobile/email_lists/1/mailings/{news_id}.json"
        r = requests.get(url)
        try:
            news_item = r.json()
            return news_item
            # news_item = self.get_post_by_id(self.channel_id, news_id)
        except Exception as e:
            print(json.dumps(e))

news = VIOMS_News()
news.add_vioms_channel(151)
news.add_vioms_channel(163)
news.check_news()
#print(json.dumps(news.news))
for n in news.news[:2]:
    item = news.get_news_item(n[1][1]['id'])
    print(item)
