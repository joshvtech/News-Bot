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
                guildSettings = await self.bot.sql_conn.fetchrow("SELECT * FROM serverList WHERE id = $1;", str(ctx.guild.id))
                sources = guildSettings["subsources"].split(",")
                if argsFriendly in sources:
                    await self.bot._reply(ctx, "You're already subscribed to that source! :warning:")
                else:
                    if "" in sources:
                        sources.remove("")
                    sources.append(argsFriendly)
                    sources = ",".join(sources)
                    await self.bot.sql_conn.execute("UPDATE serverList SET subSources = $1 WHERE id = $2;", sources, str(ctx.guild.id))
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
                guildSettings = await self.bot.sql_conn.fetchrow("SELECT * FROM serverList WHERE id = $1;", str(ctx.guild.id))
                sources = guildSettings["subsources"].split(",")
                if argsFriendly in sources:
                    sources.remove(argsFriendly)
                    sources = ",".join(sources)
                    await self.bot.sql_conn.execute("UPDATE serverList SET subSources = $1 WHERE id = $2;", sources, str(ctx.guild.id))
                    await self.bot._reply(ctx, f"Successfully unsubscribed from `{argsFriendly}`! :no_bell:")
                else:
                    await self.bot._reply(ctx, "You're not subscribed to that source! :no_bell:")
            else:
                await self.bot._reply(ctx, "Please specify a supported source! :warning:")
        else:
            await self.bot._reply(ctx, "Please specify what source like to unsubscribe from! :warning:")

    @commands.command(aliases=["setchannel", "subchannel"])
    async def setnewschannel(self, ctx):
        await self.bot.sql_conn.execute("UPDATE serverList SET subChannel = $1 WHERE id = $2;", str(ctx.channel.id), str(ctx.guild.id))
        await self.bot._reply(ctx, f"Successfully changed subscription channel to `{ctx.channel.name}`! :bell:")

def setup(bot):
    bot.add_cog(subscription(bot))
