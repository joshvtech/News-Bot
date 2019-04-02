#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load

#Import custom libraries
import libs.uptime

#Define variables
botSettings = load(open("./data/botSettings.json"))

class basic:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, arg=None):
        embed = discord.Embed(
            description = f"""
                The current prefix is `{botSettings['prefix']}`.
                You can read the bot documentation here:
                <{botSettings['docsLink']}>
            """,
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Bot Help",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Please note that you cannot use commands in DM's!"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            description = "`Calculating...`",
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Pong!",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Beep boop!"
        )
        msg = await ctx.send(embed=embed)
        responseTime = (msg.created_at - ctx.message.created_at).total_seconds()
        embed = discord.Embed(
            description = f"`{responseTime*1000}ms`",
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Pong!",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Beep boop!"
        )
        await msg.edit(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            description = f"""
                News-Bot announces news stories as soon as they're published.
                It can also help moderate your chat.
                You can invite News-Bot to your server by clicking [this link]({botSettings['inviteLink']}).
                If you need help with News-Bot, join our server [here]({botSettings['serverLink']}).
            """,
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Bot Invite",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Beep Boop!"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(
            description = f"""
                Servers: `{len(self.bot.guilds)}`
                Users: `{len(self.bot.users)}`
                Uptime: `{libs.uptime.getTime()}`
                Shard: `{ctx.message.guild.shard_id+1}/{self.bot.shard_count}`
                Prefix: `{botSettings["prefix"]}`
                Creator: `{'{0.name}#{0.discriminator}'.format(self.bot.get_user(botSettings['creator']))}`
            """,
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Bot Information",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Beep Boop!"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"SELECT * FROM serverList WHERE id = '{ctx.message.guild.id}';")
            embed = discord.Embed(
                description = "\n".join([f"{r}: `{v}`" for r, v in zip(["id", "censorship", "censoredMessage", "subChannel"], list(cur.fetchone()))]),
                color = discord.Colour(botSettings["embedColour"])
            )
            embed.set_author(
                name = "Server Info",
                icon_url = self.bot.user.avatar_url
            )
            embed.set_footer(
                text = "Only server admins can change these settings.",
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def motd(self, ctx):
        embed = discord.Embed(
            description = f"`{botSettings['motd']}` :bulb:",
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Message of The Day",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Keep being inspired!"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx):
        embed = discord.Embed(
            description = "\n".join(botSettings["votingLinks"]),
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Voting Links",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Voting is greatly appreciated, as it helps News-Bot grow!"
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(basic(bot))
