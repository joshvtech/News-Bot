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

def update(link, timeCorrection, ignoreDescription, name, shortName, logo):
    with urlopen(link) as session:
        soup_page = BeautifulSoup(session.read(), "xml")
    news_list = soup_page.findAll("item")
    news_list = [i for i in news_list if i.pubDate]
    news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:timeCorrection], "%a, %d %b %Y %H:%M:%S"))
    item = news_list[-1]
    article = Story(
        title = item.title.text,
        description = item.description.text if item.description and not ignoreDescription else "No description.",
        link = item.link.text,
        pubDate = datetime.strptime(item.pubDate.text[:timeCorrection], "%a, %d %b %Y %H:%M:%S"),
        name = name,
        shortName = shortName,
        logo = logo
    )
    return(article)

def updateAll():
    return([
        update("http://feeds.bbci.co.uk/news/world/rss.xml",             -4, False, "BBC News",       "bbcNews",       "https://i2.feedspot.com/15793.jpg"),   #BBC News
        update("https://www.cnet.com/rss/gaming/",                       -6, False, "CNET",           "cnet",          "https://i1.feedspot.com/3708244.jpg"), #CNET
        update("https://rss.nytimes.com/services/xml/rss/nyt/World.xml", -4, False, "New York Times", "newYorkTimes",  "https://i2.feedspot.com/4719130.jpg"), #New York Times
        update("http://feeds.skynews.com/feeds/rss/world.xml",           -6, False, "Sky News",       "skyNews",       "https://i3.feedspot.com/4280451.jpg"), #Sky News
        update("https://www.telegraph.co.uk/news/rss.xml",               -4, True,  "The Telegraph",  "theTelegraph",  "https://i3.feedspot.com/4880356.jpg"), #The Telegraph
        update("https://www.wired.com/feed/rss",                         -6, False, "WIRED",          "wired",         "https://i1.feedspot.com/4724360.jpg"), #WIRED
        update("https://www.cbsnews.com/latest/rss/main",                -6, False, "CBS News",       "cbsNews",       "https://i3.feedspot.com/4873151.jpg"), #CBS News
        update("http://rss.cnn.com/rss/edition_world.rss",               -4, True,  "CNN",            "cnn",           "https://i3.feedspot.com/3298.jpg"),    #CNN
        update("https://www.space.com/feeds/all",                        -6, False, "Space.com",      "spaceCom",      "https://i2.feedspot.com/4707531.jpg"), #Space.com
        update("http://feeds.ign.com/ign/games-all",                     -4, False, "IGN",            "ign",           "https://i1.feedspot.com/1180874.jpg"), #IGN
        update("https://hollywoodlife.com/feed/",                        -6, True,  "Hollywood Life", "hollywoodLife", "https://i2.feedspot.com/45422.jpg")    #Perez Hilton
    ])
