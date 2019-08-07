## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries
import aiohttp
from asyncio import sleep
from bs4 import BeautifulSoup
from datetime import datetime

## NOTE: Import Custom Libraries
from libs import sourceAlias

## NOTE: Define Variables
sources = [
    #rss url, pubDate ignore, description ignore, name, shortName, logo url
    ["http://feeds.bbci.co.uk/news/world/rss.xml",             -4, False, "BBC News",       "bbcNews",       "https://i2.feedspot.com/15793.jpg"],   #BBC News
    ["https://www.cnet.com/rss/gaming/",                       -6, False, "CNET",           "cnet",          "https://i1.feedspot.com/3708244.jpg"], #CNET
    ["https://rss.nytimes.com/services/xml/rss/nyt/World.xml", -6, False, "New York Times", "newYorkTimes",  "https://i2.feedspot.com/4719130.jpg"], #New York Times
    ["http://feeds.skynews.com/feeds/rss/world.xml",           -6, False, "Sky News",       "skyNews",       "https://i3.feedspot.com/4280451.jpg"], #Sky News
    ["https://www.telegraph.co.uk/news/rss.xml",               -4, True,  "The Telegraph",  "theTelegraph",  "https://i3.feedspot.com/4880356.jpg"], #The Telegraph
    ["https://www.wired.com/feed/rss",                         -6, False, "WIRED",          "wired",         "https://i1.feedspot.com/4724360.jpg"], #WIRED
    ["https://www.cbsnews.com/latest/rss/main",                -6, False, "CBS News",       "cbsNews",       "https://i3.feedspot.com/4873151.jpg"], #CBS News
    ["http://rss.cnn.com/rss/edition_world.rss",               -4, True,  "CNN",            "cnn",           "https://i3.feedspot.com/3298.jpg"],    #CNN
    ["https://www.space.com/feeds/all",                        -6, False, "Space.com",      "spaceCom",      "https://i2.feedspot.com/4707531.jpg"], #Space.com
    ["http://feeds.ign.com/ign/games-all",                     -4, False, "IGN",            "ign",           "https://i1.feedspot.com/1180874.jpg"], #IGN
    ["https://hollywoodlife.com/feed/",                        -6, True,  "Hollywood Life", "hollywoodLife", "https://i2.feedspot.com/45422.jpg"],   #Hollywood Life
    ["http://feeds.foxnews.com/foxnews/world.rss",             -4, True,  "FOX News",       "foxNews",       "https://i1.feedspot.com/118508.jpg"]   #FOX News
]
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
firstRun = True
feed = []

## NOTE: Define Functions
def create_news_embed(self, article):
    embed = self.bot._create_embed(title=article.name, footer=f"News-Bot does not represent nor endorse {article.name}.")
    embed.set_thumbnail(url=article.logo)
    embed.add_field(name=article.title, value=article.description)
    embed.add_field(name="Read This Story", value=article.link)
    embed.timestamp = article.pubDate
    return(embed)

## NOTE: Define Cog
class news(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.update())

    async def updateAll(self):
        results = []
        for i in sources:
            async with aiohttp.ClientSession() as session:
                async with session.get(i[0]) as response:
                    rss = await response.text()
            soup_page = BeautifulSoup(rss, "xml")
            news_list = soup_page.findAll("item")
            news_list = [i for i in news_list if i.pubDate]
            try:
                news_list.sort(key=lambda x: datetime.strptime(x.pubDate.text[:i[1]], "%a, %d %b %Y %H:%M:%S"))
            except:
                print(f"`{i[4]}` failed in sorting.")
                continue
            try:
                item = news_list[-1]
            except:
                print(f"`{i[4]}` failed in selecting.")
                continue
            article = Story(
                title = item.title.text,
                description = item.description.text if item.description and not i[2] else "No description.",
                link = item.link.text,
                pubDate = datetime.strptime(item.pubDate.text[:i[1]], "%a, %d %b %Y %H:%M:%S"),
                name = i[3],
                shortName = i[4],
                logo = i[5]
            )
            results.append(article)
        return(results)

    async def update(self):
        global firstRun
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            results = await self.updateAll()
            for article in results:
                if article not in feed:
                    feed.append(article)
                    if not firstRun:
                        embed = create_news_embed(self, article)
                        results = await self.bot.sql_conn.fetch("SELECT * FROM serverList;")
                        for i in results:
                            channel = self.bot.get_channel(int(i["subchannel"]))
                            try:
                                if article.shortName in i["subsources"].split(","):
                                    await channel.send(embed=embed)
                            except:
                                continue
            firstRun = False
            await sleep(60)

    @commands.command(aliases=["recent"])
    async def latest(self, ctx, *, args=None):
        if args:
            argsFriendly = sourceAlias.check(args.lower())
            if argsFriendly:
                await ctx.send(embed=create_news_embed(self, [i for i in feed if i.shortName == argsFriendly][-1]))
            else:
                await self.bot._reply(ctx, "Please specify a supported source! :warning:")
        else:
            await self.bot._reply(ctx, "Please specify what source you'd like to see! :warning:")

    @commands.command()
    async def sources(self, ctx):
        await ctx.send(embed=self.bot._create_embed(ctx=ctx, description=f"""
            Here's a list of supported sources:
            {', '.join([f'`{i[3]}`' for i in sources])}.
            You can find the list of aliases on our website, [here]({self.bot._settings['links']['sources']}).
            To subscribe to a source you can do `{self.bot._prefix}subscribe [*source]`.
            Example: `{self.bot._prefix}subscribe bbc`."""
        ))

def setup(bot):
    bot.add_cog(news(bot))
