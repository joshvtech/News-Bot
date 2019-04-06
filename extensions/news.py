#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
from asyncio import sleep
from datetime import datetime

#Import custom libraries
import libs.washingtonPost, libs.dailyMirror, libs.bbcNews

#Define variables
botSettings = load(open("./data/botSettings.json"))
class Story:
    def __init__(self, title, description, link, pubDate, outletName, outletLogo):
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate
        self.outletName = outletName
        self.outletLogo = outletLogo
    def __eq__(self, other):
        return(self.title == other.title)
firstRun = True
feed = list()

#Define functions
def createNewsEmbed(self, article):
    embed = discord.Embed(
        color = discord.Colour(botSettings["embedColour"])
    )
    embed.set_author(
        name = article.outletName,
        icon_url = self.bot.user.avatar_url
    )
    embed.set_footer(
        text = f"News-Bot does not represent nor endorse {article.outletName}."
    )
    embed.set_thumbnail(
        url = article.outletLogo
    )
    embed.timestamp = article.pubDate
    embed.add_field(
        name = article.title,
        value = (article.description if article.description else "No description")
    )
    embed.add_field(
        name = "Read This Story",
        value = article.link
    )
    return(embed)

class news:
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.update())

    async def update(self):
        global firstRun
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for article in [libs.washingtonPost.update(Story), libs.dailyMirror.update(Story), libs.bbcNews.update(Story)]:
                if not article in feed:
                    feed.append(article)
                    if not firstRun:
                        embed = createNewsEmbed(self, article)
                        with self.bot.sqlConnection.cursor() as cur:
                            cur.execute("SELECT * FROM serverList")
                            for i in cur.fetchall():
                                channel = self.bot.get_channel(int(i[3]))
                                try:
                                    await channel.send(embed=embed)
                                except:
                                    continue
            firstRun = False
            await sleep(60)

    @commands.command()
    async def latest(self, ctx):
        await ctx.send(embed = createNewsEmbed(self, feed[-1]))

def setup(bot):
    bot.add_cog(news(bot))
