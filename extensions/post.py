#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
import dbl
from asyncio import sleep
from os import environ

class post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #discordbots.org
        self.dbo = dbl.Client(self.bot, environ["DBO_TOKEN"])
        self.bg_task = self.bot.loop.create_task(self.discordbotsorg())
        #make bg_task into array with each task object

    async def discordbotsorg(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.dbo.post_server_count()
            await sleep(1800)

def setup(bot):
    bot.add_cog(post(bot))
