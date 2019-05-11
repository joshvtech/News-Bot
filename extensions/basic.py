## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries
import aiohttp
from psutil import cpu_percent, virtual_memory
from platform import python_version

## NOTE: Import Custom Libraries

## NOTE: Define Variables

## NOTE: Define Functions

## NOTE: Define Cog
class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, arg=None):
        embed = self.bot._create_embed(
            title="Help",
            description = f"""
                The current prefix is `{self.bot._prefix}`.
                You can get started with the bot by clicking [here]({self.bot._settings['links']['getting-started']}).
                You can view our Trello [here]({self.bot._settings['links']['trello']}) for upcoming updates.
                You can also check out the source code on GitHub [here]({self.bot._settings['links']['github']}).""",
            footer="Please note that you cannot use commands in DM's!"
        )
        if arg:
            arg = arg.lower()
            if arg in ["admin", "email"]:
                cog = self.bot.get_cog(arg)
                if cog:
                    if cog.cog_check(ctx):
                        for i in cog.get_commands():
                            embed.add_field(name=i.name.title(), value=f"{i.help}\n`{self.bot._prefix}{i.usage}`", inline=False)
                        try:
                            await ctx.author.send(embed=embed)
                        except discord.Forbidden:
                            await self.bot._reply(ctx, "I cannot DM you, please change your privacy settings and try again! :warning:")
                        else:
                            await self.bot._reply(ctx, "Check your DM's! :incoming_envelope:")
                        return
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        msg = await ctx.send(embed=self.bot._create_embed(ctx=ctx, title="Ping!", description="Delay: `Calculating...` :ping_pong:"))
        responseTime = (msg.created_at - ctx.message.created_at).total_seconds()
        await msg.edit(embed=self.bot._create_embed(ctx=ctx, title="Pong!", description=f"Delay: `{responseTime*1000}ms` :ping_pong:"))

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(embed=self.bot._create_embed(
            ctx=ctx,
            description=f"""
                News-Bot announces news stories as soon as they're published.
                It can also help moderate your chat.
                You can invite News-Bot to your server by clicking [this link]({self.bot._settings['links']['invite']}).
                If you need help with News-Bot, join our server [here]({self.bot._settings['links']['server']})."""
        ))

    @commands.command(aliases=["stats", "info"])
    async def botinfo(self, ctx):
        embed=self.bot._create_embed(
            ctx=ctx,
            description=f"""
                Hey, I'm News-Bot, owned by `{self.bot.get_user(self.bot._settings['creator'])}`.
                ```
 _   _                         ____        _
| \ | | _____      _____      | __ )  ___ | |_
|  \| |/ _ \ \ /\ / / __|_____|  _ \ / _ \| __|
| |\  |  __/\ V  V /\__ \_____| |_) | (_) | |_
|_| \_|\___| \_/\_/ |___/     |____/ \___/ \__|```"""
        )
        embed.add_field(
            name="Stats",
            value=f"""
                Prefix: `{self.bot._prefix}`
                Servers: `{len(self.bot.guilds)}`
                Users: `{len(self.bot.users)}`
                Uptime: `{self.bot._get_uptime()}`
                Latency: `{round(self.bot.latency*1000)}ms`
                Shard ID: `{ctx.guild.shard_id}`
                Messages Processed: `{self.bot._message_count}`
                Commands Processed: `{self.bot._command_count}`"""
        )
        msg = await ctx.send(embed=embed)
        if ctx.author.id in self.bot._settings["admins"]:
            memory = virtual_memory()
            embed.add_field(
                name="Advanced",
                value=f"""
                    <:python:568799857721081872> Python Version: `{python_version()}`
                    <:discord:569501148214460427> discord.py Version: `{discord.__version__}`
                    CPU Usage: `{cpu_percent(interval=1)}%`
                    RAM Usage: `{round(memory.used/1024**3, 1)}GB` of `{round(memory.total/1024**3, 1)}GB` (`{memory.percent}%`)"""
            )
            await msg.edit(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        guildSettings = await self.bot.sql_conn.fetchrow("SELECT * FROM serverList WHERE id = $1;", str(ctx.guild.id))
        await ctx.send(embed=self.bot._create_embed(ctx=ctx, description="\n".join([f"{r}: `{None if v == '' else v}`" for r, v in zip(guildSettings.keys(), guildSettings)])))

    @commands.command(aliases=["motd"])
    async def qotd(self, ctx):
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://quotes.rest/qod.json")
            json = await response.json()
            json = json["contents"]["quotes"][0]
            await ctx.send(embed=self.bot._create_embed(ctx=ctx, title="Quote of The Day", description=f"`{json['quote']}` - `{json['author']}` :bulb:"))

    @commands.command()
    async def vote(self, ctx):
        await ctx.send(embed=self.bot._create_embed(
            ctx=ctx,
            description=f"You can vote for News-Bot [here]({self.bot._settings['links']['vote']}).",
            footer="Voting is greatly appreciated, as it helps News-Bot grow!"
        ))

def setup(bot):
    bot.add_cog(basic(bot))
