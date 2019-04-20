## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries

## NOTE: Import Custom Libraries
import libs.sourceAlias

## NOTE: Define Variables

## NOTE: Define Functions

## NOTE: Define Cog
class subscription(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return(ctx.author.guild_permissions.administrator or ctx.author.id in self.bot._settings["admins"])

    @commands.command(aliases=["sub"])
    async def subscribe(self, ctx, *, args=None):
        if args:
            argsFriendly = libs.sourceAlias.check(args.lower())
            if argsFriendly:
                with self.bot.sqlConnection.cursor() as cur:
                    cur.execute(f"SELECT * FROM serverList WHERE id = '{ctx.guild.id}';")
                    sources = cur.fetchone()[4].split(",")
                    if argsFriendly in sources:
                        await self.bot._reply(ctx, "You're already subscribed to that source! :warning:")
                    else:
                        if "" in sources:
                            sources.remove("")
                        sources.append(argsFriendly)
                        sources = ",".join(sources)
                        cur.execute(f"UPDATE serverList SET subSources = '{sources}' WHERE id = '{ctx.guild.id}';")
                        await self.bot._reply(ctx, f"Successfully subscribed to `{argsFriendly}`! :bell:")
            else:
                await self.bot._reply(ctx, "Please specify a supported source! :warning:")
        else:
            await self.bot._reply(ctx, "Please specify what source like to subscribe to! :warning:")

    @commands.command(aliases=["unsub"])
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
                        await self.bot._reply(ctx, f"Successfully unsubscribed from `{argsFriendly}`! :no_bell:")
                    else:
                        await self.bot._reply(ctx, "You're not subscribed to that source! :no_bell:")
            else:
                await self.bot._reply(ctx, "Please specify a supported source! :warning:")
        else:
            await self.bot._reply(ctx, "Please specify what source like to unsubscribe from! :warning:")

    @commands.command(aliases=["setchannel"])
    async def setnewschannel(self, ctx):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"UPDATE serverList SET subChannel = '{ctx.channel.id}' WHERE id = '{ctx.guild.id}';")
            await self.bot._reply(ctx, f"Successfully changed subscription channel to `{ctx.channel.name}`! :bell:")

def setup(bot):
    bot.add_cog(subscription(bot))
