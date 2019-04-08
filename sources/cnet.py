from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def update(Story):
    with urlopen("https://www.cnet.com/rss/news/") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text[:-7],
        description = item.description.text,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S"),
        name = "CNET",
        shortName = "cnet",
        logo = "https://i1.feedspot.com/3708244.jpg"
    )
    return(article)
