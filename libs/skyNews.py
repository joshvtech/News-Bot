from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

class Story:
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link
    def __eq__(self, other):
        return(self.title == other.title or self.description == other.description)

def update():
    with urlopen("http://feeds.skynews.com/feeds/rss/world.xml") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text,
        link = item.link.text
    )
    return(article)
