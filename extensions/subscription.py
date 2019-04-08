#Import standard libraries
import discord
from discord.ext import commands

#Import custom libraries
import libs.sourceAlias

#Define functions
async def reply(message, string):
    await message.channel.send(f"{message.author.mention}, {string}")

class subscription:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sub"])
    @commands.has_permissions(administrator=True)
    async def subscribe(self, ctx, *, args=None):
        if args:
            argsFriendly = libs.sourceAlias.check(args.lower())
            if argsFriendly:
                with self.bot.sqlConnection.cursor() as cur:
                    cur.execute(f"SELECT * FROM serverList WHERE id = '{ctx.guild.id}';")
                    sources = cur.fetchone()[4].split(",")
                    if argsFriendly in sources:
                        await reply(ctx.message, "You're already subscribed to that source! :warning:")
                    else:
                        if "" in sources:
                            sources.remove("")
                        elif "Empty" in sources:
                            sources.remove("Empty")
                        sources.append(argsFriendly)
                        sources = ",".join(sources)
                        cur.execute(f"UPDATE serverList SET subSources = '{sources}' WHERE id = '{ctx.guild.id}';")
                        await reply(ctx.message, f"Successfully subscribed to `{argsFriendly}`! :bell:")
            else:
                await reply(ctx.message, "Please specify a supported source! :warning:")
        else:
            await reply(ctx.message, "Please specify what source like to subscribe to! :warning:")

    @commands.command(aliases=["unsub"])
    @commands.has_permissions(administrator=True)
    async def unsubscribe(self, ctx, *, args=None):
        if args:
            argsFriendly = libs.sourceAlias.check(args.lower())
            if argsFriendly:
                with self.bot.sqlConnection.cursor() as cur:
                    cur.execute(f"SELECT * FROM serverList WHERE id = '{ctx.guild.id}';")
                    sources = cur.fetchone()[4].split(",")
                    if argsFriendly in sources:
                        sources.remove(argsFriendly)
                        sources = ",".join(sources)
                        cur.execute(f"UPDATE serverList SET subSources = '{sources}' WHERE id = '{ctx.guild.id}';")
                        await reply(ctx.message, f"Successfully unsubscribed from `{argsFriendly}`! :no_bell:")
                    else:
                        await reply(ctx.message, "You're not subscribed to that source! :no_bell:")
            else:
                await reply(ctx.message, "Please specify a supported source! :warning:")
        else:
            await reply(ctx.message, "Please specify what source like to unsubscribe from! :warning:")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"UPDATE serverList SET subChannel = '{ctx.channel.id}' WHERE id = '{ctx.guild.id}';")
            await reply(ctx.message, f"Successfully changed subscription channel to `{ctx.channel.name}`! :bell:")

def setup(bot):
    bot.add_cog(subscription(bot))
