#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
from asyncio import sleep

#Import custom libraries
import libs.skyNews

#Define variables
botSettings = load(open("./data/botSettings.json"))
firstRun = True
feed = list()

#Define functions
def createNewsEmbed(self, article):
    embed = discord.Embed(
        description = article.description,
        color = discord.Colour(botSettings["embedColour"])
    )
    embed.set_author(
        name = article.title,
        icon_url = self.bot.user.avatar_url
    )
    embed.set_footer(
        text = "News-Bot does not represent Sky News or endorse any opinions expressed by Sky News."
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
            article = libs.skyNews.update()
            if article not in feed:
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
                else:
                    firstRun = False
            await sleep(120)

    @commands.command()
    async def latest(self, ctx):
        await ctx.send(embed = createNewsEmbed(self, feed[-1]))

def setup(bot):
    bot.add_cog(news(bot))
