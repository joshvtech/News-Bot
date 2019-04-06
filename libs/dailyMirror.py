from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def update(Story):
    with urlopen("http://www.mirror.co.uk/news/world-news/rss.xml") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"),
        outletName = "The Daily Mirror",
        outletLogo = "https://i1.feedspot.com/1716354.jpg?t=1503045119"
    )
    return(article)
