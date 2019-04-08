from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def update(Story):
    with urlopen("https://rss.nytimes.com/services/xml/rss/nyt/World.xml") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"),
        name = "New York Times",
        shortName = "newYorkTimes",
        logo = "https://i2.feedspot.com/4719130.jpg?t=1534564857"
    )
    return(article)
