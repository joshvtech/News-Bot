#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
from cpuinfo import get_cpu_info
from psutil import cpu_percent, virtual_memory
from platform import python_version, platform
from inspect import isawaitable

#Import custom libraries
import libs.uptime

#Define variables
adminCommands = load(open("./data/adminCommands.json"))
botSettings = load(open("./data/botSettings.json"))
cpuinfo = get_cpu_info()

#Define functions
def isAdmin(ctx):
    return(ctx.author.id in botSettings["admins"])
async def reply(message, string):
    await message.channel.send(f"{message.author.mention}, {string}")

class admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(isAdmin)
    async def adminhelp(self, ctx, arg=None):
        embed = discord.Embed(
            description = f"""
                These are the commands you can use with News-Bot as an admin.
                You can use `{botSettings['prefix']}adminhelp [command]` to see the usage of a commmand.
                The current prefix is `{botSettings['prefix']}`.
            """,
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Admin Help",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Please note that you cannot use commands in DM's!"
        )
        if arg:
            arg = arg.lower()
            results = list()
            for i in adminCommands:
                if i["name"].lower().startswith(arg):
                    results.append(i)
            if results == list():
                await reply(ctx.message, "I couldn't find any commands! :warning:")
                return
            else:
                for i in results:
                    embed.add_field(
                        name = i["name"],
                        value = f"{i['description']}\n`{botSettings['prefix']}{i['usage']}`",
                        inline = False
                    )
        else:
            for i in adminCommands:
                embed.add_field(
                    name = i["name"],
                    value = i["description"],
                    inline = False
                )
        await ctx.message.author.send(embed=embed)
        await reply(ctx.message, "Check your DM's! :incoming_envelope:")

    @commands.command()
    @commands.check(isAdmin)
    async def restart(self, ctx):
        embed = discord.Embed(
            description = f"The admin '{ctx.author.name}#{ctx.author.discriminator}' has restarted the bot.",
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Currently being restarted.",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "If this wasn't authorized, call the police!"
        )
        await self.bot.get_user(botSettings["creator"]).send(embed=embed)
        await reply(ctx.message, "Restarting... :arrows_counterclockwise:")
        print("Restarting...")
        await self.bot.close()

    @commands.command()
    @commands.check(isAdmin)
    async def hostinfo(self, ctx):
        embed = discord.Embed(
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Host Information",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Haha, only bot admins can do this!"
        )
        embed.add_field(
            name = "Operating System",
            value = f"Name: `{platform()}`",
            inline = False
        )
        embed.add_field(
            name = "Versions",
            value = f"""
                Python: `{python_version()}`
                Library: `discord.py {discord.__version__}`
            """,
            inline = False
        )
        embed.add_field(
            name = "CPU",
            value = f"""
                Model: `{cpuinfo['brand']}`
                Cores: `{cpuinfo['count']}`
                Architecture: `{cpuinfo['arch']}`
                Usage: `{cpu_percent(interval=1)}%`
            """,
            inline = False
        )
        memory = virtual_memory()
        embed.add_field(
            name = "RAM",
            value = f"""
                Used: `{round((memory.used)/1024**3, 1)}GB`
                Total: `{round((memory.total)/1024**3, 1)}GB`
            """,
            inline = False
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(isAdmin)
    async def setpresence(self, ctx, status=None, *, game=None):
        if status:
            status = status.lower()
            if status in ["online", "idle", "dnd"]:
                await self.bot.change_presence(status = discord.Status[status], activity = discord.Game(f"{botSettings['prefix']}help{(f' | {game}' if game else '')}"))
                embed = discord.Embed(
                    description = "Successfully changed bot presence.",
                    color = discord.Colour(botSettings["embedColour"])
                )
                embed.set_author(
                    name = "Set Presence",
                    icon_url = self.bot.user.avatar_url
                )
                embed.set_footer(
                    text = "Haha, only bot admins can do this!"
                )
                embed.add_field(
                    name = "Status",
                    value = f"`{status}`",
                    inline = False
                )
                embed.add_field(
                    name = "Game",
                    value = f"`{game}`",
                    inline = False
                )
                await ctx.send(embed=embed)
            else:
                await reply(ctx.message, "That status wasn't recognised! :warning:")
        else:
            await reply(ctx.message, "Please specify the status! :warning:")

    @commands.command()
    @commands.check(isAdmin)
    async def reload(self, ctx, arg=None):
        if arg:
            arg = f"extensions.{arg.lower()}"
            if arg == "extensions.news":
                self.bot.get_cog("news").bg_task.cancel()
            elif arg == "extensions.post":
                self.bot.get_cog("post").bg_task.cancel()
            self.bot.unload_extension(arg)
            self.bot.load_extension(arg)
            embed = discord.Embed(
                description = f"The admin '{ctx.author.name}#{ctx.author.discriminator}' has reloaded `{arg}`.",
                color = discord.Colour(botSettings["embedColour"])
            )
            embed.set_author(
                name = "Extension currently being reloaded.",
                icon_url = self.bot.user.avatar_url
            )
            embed.set_footer(
                text = "If this wasn't authorized, call the police!"
            )
            await self.bot.get_user(botSettings["creator"]).send(embed=embed)
            embed = discord.Embed(
                description = f"Successfully reloaded extension `{arg}`.",
                color = discord.Colour(botSettings["embedColour"])
            )
            embed.set_author(
                name = "Reload Extension",
                icon_url = self.bot.user.avatar_url
            )
            embed.set_footer(
                text = "Haha, only bot admins can do this!"
            )
            await ctx.send(embed=embed)
        else:
            await reply(ctx.message, "Please specify the extension to reload! :warning:")

    @commands.command()
    @commands.check(isAdmin)
    async def eval(self, ctx, *, args=None):
        embed = discord.Embed(
            color = discord.Colour(botSettings["embedColour"])
        )
        embed.set_author(
            name = "Evaluate",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_footer(
            text = "Haha, only bot admins can do this!"
        )
        embed.add_field(
            name = "Input",
            value = f"```python\n{args}```",
            inline = False
        )
        cmd = eval(args)
        if isawaitable(cmd):
            cmd = await cmd
        embed.add_field(
            name = "Output",
            value = f"```python\n{cmd}```",
            inline = False
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(isAdmin)
    async def announce(self, ctx, *, args=None):
        if args:
            embed = discord.Embed(
                description = args,
                color = discord.Colour(botSettings["embedColour"])
            )
            embed.set_author(
                name = "Announcement",
                icon_url = self.bot.user.avatar_url
            )
            embed.set_footer(
                text = f"From '{ctx.author.name}#{ctx.author.discriminator}'."
            )
            with self.bot.sqlConnection.cursor() as cur:
                cur.execute("SELECT * FROM serverList")
                for i in cur.fetchall():
                    channel = self.bot.get_channel(int(i[3]))
                    try:
                        await channel.send(embed=embed)
                    except:
                        continue
                await reply(ctx.message, "Done! :mailbox_with_mail:")
        else:
            await reply(ctx.message, "Please specify the message to send! :warning:")

def setup(bot):
    bot.add_cog(admin(bot))
