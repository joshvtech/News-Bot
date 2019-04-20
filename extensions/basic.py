## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries
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
    async def help(self, ctx):
        await ctx.send(embed=self.bot._create_embed(
            title="Help",
            description = f"""
                The current prefix is `{self.bot._prefix}`.
                You can find a list of commands [here]({self.bot._settings['links']['website']}).
                You can view our Trello [here]({self.bot._settings['links']['trello']}) for upcoming updates.
                You can also check out the source code on GitHub [here]({self.bot._settings['links']['github']}).""",
            footer="Please note that you cannot use commands in DM's!"
        ))

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
                :robot: Prefix: `{self.bot._prefix}`
                <:servers:568801413124194347> Servers: `{len(self.bot.guilds)}`
                :busts_in_silhouette: Users: `{len(self.bot.users)}`
                :stopwatch: Uptime: `{self.bot._get_uptime()}`
                :ping_pong: Latency: `{round(self.bot.latency*1000)}ms`
                :gem: Shard ID: `{ctx.guild.shard_id}`
                :open_file_folder: Messages Processed: `{self.bot._message_count}`
                :open_file_folder: Commands Processed: `{self.bot._command_count}`"""
        )
        msg = await ctx.send(embed=embed)
        if ctx.author.id in self.bot._settings["admins"]:
            memory = virtual_memory()
            embed.add_field(
                name="Advanced",
                value=f"""
                    <:python:568799857721081872> Python Version: `{python_version()}`
                    <:discord:568799938008580096> discord.py Version: `{discord.__version__}`
                    CPU Usage: `{cpu_percent(interval=1)}%`
                    RAM Usage: `{round(memory.used/1024**3, 1)}GB` of `{round(memory.total/1024**3, 1)}GB` (`{memory.percent}%`)"""
            )
            await msg.edit(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        with self.bot.sqlConnection.cursor() as cur:
            cur.execute(f"SELECT * FROM serverList WHERE id = '{ctx.message.guild.id}';")
            await ctx.send(embed=self.bot._create_embed(
                ctx=ctx,
                description="\n".join([f"{r}: `{None if v == '' else v}`" for r, v in zip(["id", "censorship", "censoredMessage", "subChannel", "subSources"], list(cur.fetchone()))])
            ))

    @commands.command()
    async def motd(self, ctx):
        await ctx.send(embed=self.bot._create_embed(ctx=ctx, title="Message of The Day", description=f"`{self.bot._settings['motd']}` :bulb:"))

    @commands.command()
    async def vote(self, ctx):
        await ctx.send(embed=self.bot._create_embed(
            ctx=ctx,
            description=f"You can vote for News-Bot [here]({self.bot._settings['links']['vote']}).",
            footer="Voting is greatly appreciated, as it helps News-Bot grow!"
        ))

def setup(bot):
    bot.add_cog(basic(bot))
