#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load

#Import custom libraries
import libs.censorshipCheck

#Define variables
botSettings = load(open("./data/botSettings.json"))

#Define functions
async def reply(message, string):
    await message.channel.send(f"{message.author.mention}, {string}")

class censorship:
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute("INSERT INTO serverList VALUES (%s, %s, %s, %s);", (str(guild.id), False, "Please keep it clean! :underage:", "0"))

    async def on_guild_remove(self, guild):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"DELETE FROM serverList WHERE id = '{str(guild.id)}';")

    @commands.command(aliases=["enablecensorship"])
    @commands.has_permissions(administrator=True)
    async def enablecensoring(self, ctx, arg=None):
        if arg:
            arg = arg.lower()
            if arg == "true" or arg == "false":
                with self.bot.sqlConnection.cursor() as cur:
                    cur.execute(f"""
                        UPDATE serverList
                        SET censorship = {arg=="true"}
                        WHERE id = '{ctx.message.guild.id}';
                    """)
                    embed = discord.Embed(
                        description = f"Successfully changed censorship status to `{arg.title()}`.",
                        color = discord.Colour(botSettings["embedColour"])
                    )
                    embed.set_author(
                        name = "Enable Censoring",
                        icon_url = self.bot.user.avatar_url
                    )
                    embed.set_footer(
                        text = "Only server admins can do this."
                    )
                    await ctx.send(embed=embed)
            else:
                await reply(ctx.message, "Please read the command usage! :warning:")
        else:
            await reply(ctx.message, "Please read the command usage! :warning:")

    @commands.command(aliases=["censormessage"])
    @commands.has_permissions(administrator=True)
    async def setcensormessage(self, ctx, *, arg=None):
        if arg:
            if libs.censorshipCheck.check(ctx.message):
                await reply(ctx.message, "Please make sure that your message is clean! :warning:")
            else:
                with self.bot.sqlConnection.cursor() as cur:
                    cur.execute(f"""
                        UPDATE serverList
                        SET censoredMessage = (%s)
                        WHERE id = '{ctx.message.guild.id}';
                    """, (arg, ))
                    embed = discord.Embed(
                        description = "Successfully changed censorship message to `{}`.".format(arg),
                        color = discord.Colour(botSettings["embedColour"])
                    )
                    embed.set_author(
                        name = "Set Censorship Message",
                        icon_url = self.bot.user.avatar_url
                    )
                    embed.set_footer(
                        text = "Only server admins can do this."
                    )
                    await ctx.send(embed=embed)
        else:
            await reply(ctx.message, "Please specify the message! :warning:")

def setup(bot):
    bot.add_cog(censorship(bot))
