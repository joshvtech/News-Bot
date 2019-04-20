## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries

## NOTE: Import Custom Libraries
import libs.censorshipCheck

## NOTE: Define Variables

## NOTE: Define Functions

## NOTE: Define Cog
class censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return(ctx.author.guild_permissions.administrator or ctx.author.id in self.bot._settings["admins"])

    @commands.command(aliases=["enablecensorship", "censorship"])
    async def enablecensoring(self, ctx, arg=None):
        if arg:
            arg = arg.lower()
            if arg in ["true", "false"]:
                with self.bot.sqlConnection.cursor() as cur:
                    cur.execute(f"""
                        UPDATE serverList
                        SET censorship = {arg=="true"}
                        WHERE id = '{ctx.message.guild.id}';
                    """)
                    await ctx.send(embed=self.bot._create_embed(ctx=ctx, description=f"Successfully changed censorship status to `{arg=='true'}`."))
            else:
                await self.bot._reply(ctx, "Please read the command usage! :warning:")
        else:
            await self.bot._reply(ctx, "Please read the command usage! :warning:")

    @commands.command(aliases=["censormessage"])
    async def setcensormessage(self, ctx, *, arg=None):
        if arg:
            if libs.censorshipCheck.check(ctx.message):
                await self.bot._reply(ctx, "Please make sure that your message is clean! :warning:")
            else:
                with self.bot.sqlConnection.cursor() as cur:
                    cur.execute(f"""
                        UPDATE serverList
                        SET censoredMessage = (%s)
                        WHERE id = '{ctx.message.guild.id}';
                    """, (arg, ))
                    await ctx.send(embed=self.bot._create_embed(ctx=ctx, description="Successfully changed censorship message to `{}`.".format(arg)))
        else:
            await self.bot._reply(ctx, "Please specify the message! :warning:")

def setup(bot):
    bot.add_cog(censorship(bot))
