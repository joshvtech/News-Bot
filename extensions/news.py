## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries
from asyncio import sleep

## NOTE: Import Custom Libraries
from libs import sources, sourceAlias

## NOTE: Define Variables
firstRun = True
feed = list()

## NOTE: Define Functions

## NOTE: Define Cog

class news(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.update())

    def createNewsEmbed(self, article):
        embed = self.bot._create_embed(title=article.name, footer=f"News-Bot does not represent nor endorse {article.name}.")
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

    async def update(self):
        global firstRun
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for article in sources.updateAll():
                if not article in feed:
                    feed.append(article)
                    if not firstRun:
                        embed = self.createNewsEmbed(article)
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
                await ctx.send(embed=self.createNewsEmbed([i for i in feed if i.shortName == argsFriendly][-1]))
            else:
                await self.bot._reply(ctx, "Please specify a supported source! :warning:")
        else:
            await self.bot._reply(ctx, "Please specify what source you'd like to see! :warning:")

def setup(bot):
    bot.add_cog(news(bot))
