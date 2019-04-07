from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def update(Story):
    with urlopen("http://feeds.skynews.com/feeds/rss/world.xml") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S"),
        outletName = "Sky News",
        outletLogo = "https://i3.feedspot.com/4280451.jpg?t=1503463513"
    )
    return(article)
