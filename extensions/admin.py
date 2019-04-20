## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries
from inspect import isawaitable

## NOTE: Import Custom Libraries

## NOTE: Define Variables

## NOTE: Define Functions

## NOTE: Define Cog
class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return(ctx.author.id in self.bot._settings["admins"])

    @commands.command(help="Displays this help message.", usage="adminhelp [command]")
    async def adminhelp(self, ctx, arg=None):
        embed = self.bot._create_embed(
            ctx=ctx,
            description=f"""
                These are the commands you can use with News-Bot as an admin.
                You can use `{self.bot._prefix}{ctx.command.usage}` to see the usage of a commmand.
                The current prefix is `{self.bot._prefix}`.""",
            footer="Please note that you cannot use commands in DM's!"
        )
        if arg:
            arg = arg.lower()
            results = [i for i in self.get_commands() if i.name.startswith(arg)]
            if len(results) > 0:
                for i in results:
                    embed.add_field(name=i.name.title(), value=f"{i.help}\n`{self.bot._prefix}{i.usage}`", inline=False)
            else:
                await self.bot._reply(ctx, "I couldn't find any commands! :warning:")
                return
        else:
            for i in self.get_commands():
                embed.add_field(name=i.name.title(), value=i.help, inline=False)
        await ctx.message.author.send(embed=embed)
        await self.bot._reply(ctx, "Check your DM's! :incoming_envelope:")

    @commands.command(help="Restart the entire bot.", usage="restart")
    async def restart(self, ctx):
        embed = self.bot._create_embed(ctx=ctx, description=f"The bot is being restarted.")
        await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
        await ctx.send(embed=embed)
        print("Restarting...")
        #self.bot.sqlConnection.close()
        await self.bot.close()

    @commands.command(help="Set the bots status.", usage="setpresence [*online/idle/dnd] [game name]")
    async def setpresence(self, ctx, status=None, *, game=None):
        if status:
            status = status.lower()
            if status in ["online", "idle", "dnd"]:
                await self.bot.change_presence(status=discord.Status[status], activity=discord.Game(f"{self.bot._prefix}help{f' | {game}' if game else ''}"))
                embed = self.bot._create_embed(ctx=ctx, description="Successfully changed bot presence.")
                embed.add_field(name="Status", value=f"`{status}`")
                embed.add_field(name="Game", value=f"`{game}`")
                await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
                await ctx.send(embed=embed)
            else:
                await self.bot._reply(ctx, "That status wasn't recognised! :warning:")
        else:
            await self.bot._reply(ctx, "Please specify the status! :warning:")

    @commands.command(help="Reload an extension.", usage="reload [*extension name]")
    async def reload(self, ctx, arg=None):
        if arg:
            arg = f"extensions.{arg.lower()}"
            if arg == "extensions.news":
                news = self.bot.get_cog("news").bg_task
                if news:
                    news.cancel()
            elif arg == "extensions.post":
                post = self.bot.get_cog("post").bg_task
                if post:
                    post.cancel()
            try:
                self.bot.unload_extension(arg)
            except:
                pass
            self.bot.load_extension(arg)
            embed = self.bot._create_embed(ctx=ctx, description=f"Successfully reloaded extension `{arg}`.")
            await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
            await ctx.send(embed=embed)
        else:
            await self.bot._reply(ctx, "Please specify the extension to reload! :warning:")

    @commands.command(help="Evaluate an expression.", usage="eval [*command]")
    async def eval(self, ctx, *, args=None):
        embed = self.bot._create_embed(ctx=ctx)
        embed.add_field(name="Input", value=f"```py\n{args}```", inline=False)
        cmd = eval(args)
        if isawaitable(cmd):
            cmd = await cmd
        embed.add_field(name="Output", value=f"```py\n{cmd}```", inline=False)
        await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
        await ctx.send(embed=embed)

    @commands.command(help="Send a message to every subscribed server.", usage="announce [*message]")
    async def announce(self, ctx, *, args=None):
        if args:
            embed = self.bot._create_embed(title="Announcement", description=args, footer=f"From '{ctx.author}'.")
            with self.bot.sqlConnection.cursor() as cur:
                cur.execute("SELECT * FROM serverList")
                for i in cur.fetchall():
                    channel = self.bot.get_channel(int(i[3]))
                    try:
                        await channel.send(embed=embed)
                    except:
                        continue
                await self.bot._reply(ctx, "Done! :mailbox_with_mail:")
        else:
            await self.bot._reply(ctx, "Please specify the message to send! :warning:")

    """@commands.command(help="Query the database.", usage="sql [*query]")
    async def sql(self, ctx, *, args=None):
        if args:
            with self.bot.sqlConnection.cursor() as cur:
                cur.execute(args)
                cur.fetchall()
                await ctx.send(embed=self.bot._create_embed(ctx=ctx, description=f"{cur.fetchall()}"))
        else:
            await self.bot._reply(ctx, "Please specify a query.")"""

    @commands.command(help="Delete a row from the database.", usage="deleterow [*id]")
    async def deleterow(self, ctx, arg=None):
        if arg:
            with self.bot.sqlConnection.cursor() as cur:
                cur.execute(f"DELETE FROM serverList WHERE id = '{arg}';")
                embed = self.bot._create_embed(ctx=ctx, description=f"Deleted row `{arg}`.")
                await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
                await ctx.send(embed=embed)
        else:
            await self.bot._reply(ctx, "Please specify an ID.")

    @commands.command(help="Forcefully make the bot leave the server.", usage="leave")
    async def leave(self, ctx):
        embed = self.bot._create_embed(ctx=ctx, description=f"Leaving `{ctx.guild.name}`... :wave:")
        await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
        await ctx.send(embed=embed)
        await ctx.guild.leave()

def setup(bot):
    bot.add_cog(admin(bot))
