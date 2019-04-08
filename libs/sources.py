from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

class Story:
    def __init__(self, title, description, link, pubDate, name, shortName, logo):
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate
        self.name = name
        self.shortName = shortName
        self.logo = logo
    def __eq__(self, other):
        return(self.link == other.link)

def updateAll():
    return([bbcNews(), cnet(), newYorkTimes(), skyNews(), theTelegraph()])

def bbcNews():
    with urlopen("http://feeds.bbci.co.uk/news/world/rss.xml") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"),
        name = "BBC News",
        shortName = "bbcNews",
        logo = "https://i2.feedspot.com/15793.jpg?t=1515756206"
    )
    return(article)

def cnet():
    with urlopen("https://www.cnet.com/rss/gaming/") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S"),
        name = "CNET",
        shortName = "cnet",
        logo = "https://i1.feedspot.com/3708244.jpg"
    )
    return(article)

def newYorkTimes():
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

def skyNews():
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
        name = "Sky News",
        shortName = "skyNews",
        logo = "https://i3.feedspot.com/4280451.jpg?t=1503463513"
    )
    return(article)

def theTelegraph():
    with urlopen("https://www.telegraph.co.uk/news/rss.xml") as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = None,
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:-4], "%a, %d %b %Y %H:%M:%S"),
        name = "The Telegraph",
        shortName = "theTelegraph",
        logo = "https://i3.feedspot.com/4880356.jpg"
    )
    return(article)
