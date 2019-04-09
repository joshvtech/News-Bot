#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
from asyncio import sleep
from datetime import datetime

#Import custom libraries
from libs import sources, sourceAlias

#Define variables
botSettings = load(open("./data/botSettings.json"))
firstRun = True
feed = list()

#Define functions
async def reply(message, string):
    await message.channel.send(f"{message.author.mention}, {string}")
def createNewsEmbed(self, article):
    embed = discord.Embed(
        color = discord.Colour(botSettings["embedColour"])
    )
    embed.set_author(
        name = article.name,
        icon_url = self.bot.user.avatar_url
    )
    embed.set_footer(
        text = f"News-Bot does not represent nor endorse {article.name}."
    )
    embed.set_thumbnail(
        url = article.logo
    )
    embed.add_field(
        name = article.title,
        value = article.description
    )
    embed.add_field(
        name = "Read This Story",
        value = article.link
    )
    embed.timestamp = article.pubDate
    return(embed)

class news:
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.update())

    async def update(self):
        global firstRun
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for article in sources.updateAll():
                if not article in feed:
                    feed.append(article)
                    if not firstRun:
                        embed = createNewsEmbed(self, article)
                        with self.bot.sqlConnection.cursor() as cur:
                            cur.execute("SELECT * FROM serverList")
                            for i in cur.fetchall():
                                channel = self.bot.get_channel(int(i[3]))
                                try:
                                    if article.shortName in i[4].split(","):
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
                await ctx.send(embed = createNewsEmbed(self, [i for i in feed if i.shortName == argsFriendly][-1]))
            else:
                await reply(ctx.message, "Please specify a supported source! :warning:")
        else:
            await reply(ctx.message, "Please specify what source you'd like to see! :warning:")

def setup(bot):
    bot.add_cog(news(bot))
