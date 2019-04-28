## NOTE: Import Standard Libraries
import discord
from discord.ext import commands

## NOTE: Import Required Libraries
import aiohttp, asyncpg
from json import load
from sys import exc_info
from traceback import print_exc
from os import environ, listdir
from datetime import datetime

## NOTE: Import Custom Libraries
import libs.censorshipCheck

## NOTE: Define Variables
settings = load(open("./data/settings.json"))
prefix = environ["PREFIX"]
start_time = datetime.now().replace(microsecond=0)

## NOTE: Create the Bot...
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True)
bot.remove_command("help")

## NOTE: Define Functions
async def reply(ctx, string):
    return(await ctx.channel.send(f"{ctx.author.mention}, {string}"))

def create_embed(ctx=None, title=None, description=None, footer=None):
    embed = discord.Embed(description=description, color=discord.Colour(settings["embedColour"]))
    embed.set_author(name=ctx.command.name.title() if ctx and not title else title, icon_url=bot.user.avatar_url)
    embed.set_footer(text=f"Executed by `{ctx.author}`." if ctx else footer)
    embed.timestamp = ctx.message.created_at if ctx else datetime.now().astimezone()
    return(embed)

def get_uptime():
    return(datetime.now().replace(microsecond=0) - start_time)

async def sql_connect():
    bot.sql_conn = await asyncpg.create_pool(f"{environ['DATABASE_URL']}?sslmode=require")

## NOTE: Set Bot Vars
bot._settings = settings
bot._prefix = prefix
bot._start_time = start_time
bot._reply = reply
bot._create_embed = create_embed
bot._get_uptime = get_uptime
bot._message_count = 0
bot._command_count = 0

## NOTE: Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await bot._reply(ctx.message, "You must be an administrator to do that! :warning:")
    elif isinstance(error, commands.CommandNotFound):
        await bot._reply(ctx.message, "I couldn't find that command! :warning:")
        await ctx.invoke(bot.get_command("help"))
    else:
        print(error)
        await bot._reply(ctx.message, f"An error occured <:spaghetti_code:568802399527895061>```\n{error}```")

@bot.event
async def on_error(event, *args):
    if (isinstance(exc_info()[1], discord.Forbidden)):
        print(f"Ignoring 403 exception in '{event}'.")
    else:
        print_exc()

## NOTE: Bot Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}. ({bot.user.id})")
    await bot.change_presence(activity = discord.Game(f"{bot._prefix}help"))
    async with aiohttp.ClientSession() as session:
        async with session.get("http://ipinfo.io/json") as response:
            json = await response.json()
    embed = bot._create_embed(title="Bot Started", description=f"The prefix is `{bot._prefix}`.", footer="If this wasn't you, call the police!")
    embed.add_field(name="IP Address", value=json["ip"])
    embed.add_field(name="Server Location", value=json["loc"])
    embed.add_field(name="Startup Time", value=get_uptime())
    await bot.get_channel(settings["logsChannel"]).send(embed=embed)

@bot.event
async def on_guild_join(guild):
    await bot.sql_conn.execute("INSERT INTO serverList VALUES ($1, false, 'Please keep it clean! :underage:', '0', '');", str(guild.id))

@bot.event
async def on_guild_remove(guild):
    await bot.sql_conn.execute("DELETE FROM serverList WHERE id = $1;", str(guild.id))

@bot.event
async def on_message(message):
    if message.guild and not message.author.bot:
        guildSettings = await bot.sql_conn.fetchrow("SELECT * FROM serverList WHERE id = $1;", str(message.guild.id))
        if guildSettings:
            if guildSettings["censorship"]:
                if libs.censorshipCheck.check(message):
                    await message.delete()
                    await bot._reply(message, guildSettings["censoredmessage"])
                    return
            await bot.process_commands(message)
            bot._message_count += 1
        else:
            await bot.sql_conn.execute("INSERT INTO serverList VALUES ($1, false, 'Please keep it clean! :underage:', '0', '');", str(message.guild.id))

@bot.event
async def on_command(ctx):
    bot._command_count += 1

## NOTE: Start Doing Important Stuff...
if __name__ == "__main__":
    ## NOTE: Add Extensions
    for i in [f"extensions.{i[:-3]}" for i in listdir("extensions") if not i == "__pycache__"]:
        try:
            bot.load_extension(i)
        except Exception as error:
            print(f"{i} cannot be loaded.\n{error}")
    ## NOTE: Connect to PostgreSQL
    bot.loop.run_until_complete(sql_connect())
    ## NOTE: Run the Bot
    bot.run(environ["BOT_TOKEN"])
