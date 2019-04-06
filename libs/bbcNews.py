from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def update(Story):
    with urlopen("http://feeds.bbci.co.uk/news/uk/rss.xml") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"),
        outletName = "BBC News",
        outletLogo = soup_page.image.url.text
    )
    return(article)
