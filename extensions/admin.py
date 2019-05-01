## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries
import ast

## NOTE: Import Custom Libraries

## NOTE: Define Variables

## NOTE: Define Functions
def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

## NOTE: Define Cog
class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return(ctx.author.id in self.bot._settings["admins"])

    @commands.command(help="Restart the entire bot.", usage="restart")
    async def restart(self, ctx):
        embed = self.bot._create_embed(ctx=ctx, description=f"The bot is being restarted.")
        await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
        await ctx.send(embed=embed)
        print("Restarting...")
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

    @commands.command(help="Reload an extension.", usage="load|reload [*extension]", aliases=["reload"])
    async def load(self, ctx, arg=None):
        if arg:
            arg = f"extensions.{arg.lower()}"
            try:
                self.bot.unload_extension(arg)
            except:
                pass
            self.bot.load_extension(arg)
            embed = self.bot._create_embed(ctx=ctx, description=f"Successfully {ctx.invoked_with}ed extension `{arg}`.")
            await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
            await ctx.send(embed=embed)
        else:
            await self.bot._reply(ctx, "Please specify the extension to reload! :warning:")

    @commands.command(help="Load an extension.", usage="unload [*extension]")
    async def unload(self, ctx, arg=None):
        if arg:
            arg = f"extensions.{arg.lower()}"
            self.bot.unload_extension(arg)
            embed = self.bot._create_embed(ctx=ctx, description=f"Successfully unloaded extension `{arg}`.")
            await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
            await ctx.send(embed=embed)
        else:
            await self.bot._reply(ctx, "Please specify the extension to unload! :warning:")

    @commands.command(help="Read, evaluate and print codeblocks.", usage="repl|python|py [*command]", aliases=["python", "py"])
    async def repl(self, ctx, *, args=None):
        args = args.strip("`")
        cmd = "\n".join([f"    {i}" for i in args.splitlines()])
        fn_name = "_repl"
        parsed = ast.parse(f"async def {fn_name}():\n{cmd}")
        body = parsed.body[0].body
        insert_returns(body)
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "message": ctx.message,
            "guild": ctx.guild,
            "channel": ctx.channel,
            "author": ctx.author
        }
        env.update(globals())
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = await eval(f"{fn_name}()", env)
        embed = self.bot._create_embed(ctx=ctx)
        embed.add_field(name="Input", value=f"```py\n{args}```", inline=False)
        embed.add_field(name="Output", value=f"```py\n{result}```", inline=False)
        await self.bot.get_channel(self.bot._settings["logsChannel"]).send(embed=embed)
        await ctx.send(embed=embed)

    @commands.command(help="Send a message to every subscribed server.", usage="announce [*message]")
    async def announce(self, ctx, *, args=None):
        if args:
            embed = self.bot._create_embed(title="Announcement", description=args, footer=f"From '{ctx.author}'.")
            results = await self.bot.sql_conn.fetch("SELECT * FROM serverList;")
            for i in results:
                channel = self.bot.get_channel(int(i["subchannel"]))
                try:
                    await channel.send(embed=embed)
                except:
                    continue
            await self.bot._reply(ctx, "Done! :mailbox_with_mail:")
        else:
            await self.bot._reply(ctx, "Please specify the message to send! :warning:")

    @commands.command(help="Delete a row from the database.", usage="deleterow [*id]")
    async def deleterow(self, ctx, arg=None):
        if arg:
            await self.bot.sql_conn.execute("DELETE FROM serverList WHERE id = $1;", str(arg))
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
