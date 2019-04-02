#Import standard libraries
import discord
from discord.ext import commands

#Define functions
async def reply(message, string):
    await message.channel.send(f"{message.author.mention}, {string}")

class subscription:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sub"])
    @commands.has_permissions(administrator=True)
    async def subscribe(self, ctx):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"""
                UPDATE serverList
                SET subChannel = '{ctx.message.channel.id}'
                WHERE id = '{ctx.message.guild.id}';
            """)
            await reply(ctx.message, "Successfully subscribed! :bell:")

    @commands.command(aliases=["unsub"])
    @commands.has_permissions(administrator=True)
    async def unsubscribe(self, ctx):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"""
                UPDATE serverList
                SET subChannel = '0'
                WHERE id = '{ctx.message.guild.id}';
            """)
            await reply(ctx.message, "Successfully unsubscribed! :no_bell:")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setnewschannel(self, ctx):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"""
                UPDATE serverList
                SET subChannel = '{ctx.message.channel.id}'
                WHERE id = '{ctx.message.guild.id}';
            """)
            await reply(ctx.message, f"Successfully changed news feed channel to '{ctx.message.channel.name}'! :bell:")

def setup(bot):
    bot.add_cog(subscription(bot))
