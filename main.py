#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
import aiohttp, psycopg2
from json import load
from sys import exc_info
from traceback import print_exc
from os import environ

#Define variables
botSettings = load(open("./data/botSettings.json"))
myExtensions = [
    "extensions.admin",
    "extensions.basic",
    "extensions.censorship",
    "extensions.news",
    "extensions.post",
    "extensions.subscription"
]

#Define functions
async def reply(message, string):
    await message.channel.send(f"{message.author.mention}, {string}")

#Import custom libraries
import libs.censorshipCheck

#----------Bot Stuff----------#

bot = commands.AutoShardedBot(
    command_prefix = environ["PREFIX"],
    case_insensitive = True
)
bot.remove_command("help")

#----------Error Handling----------#

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await reply(ctx.message, "You must be a server admin to do that! :warning:")
    elif isinstance(error, commands.CheckFailure):
        await reply(ctx.message, "You must be a bot admin to do that! :warning:")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print(error)
        await reply(ctx.message, f"An error occured :warning:```\n{error}```")

@bot.event
async def on_error(event, *args):
    if (isinstance(exc_info()[1], discord.Forbidden)):
        print(f"Ignoring 403 exception in '{event}'.")
    else:
        print_exc()

#----------Internal Events----------#

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}. ({bot.user.id})")
    await bot.change_presence(activity = discord.Game(f"{botSettings['prefix']}help"))
    async with aiohttp.ClientSession() as session:
        async with session.get("http://ipinfo.io/json") as response:
            info = await response.json()
            embed = discord.Embed(
                description = f"The prefix is `{botSettings['prefix']}`.",
                color = discord.Colour(botSettings["embedColour"])
            )
            embed.set_author(
                name = "News-Bot has started up.",
                icon_url = bot.user.avatar_url
            )
            embed.set_footer(
                text = "If this wasn't you, call the police!"
            )
            embed.add_field(
                name = "Internet Protocol",
                value = info["ip"],
                inline = False
            )
            embed.add_field(
                name = "Reported Server Location",
                value = info["loc"],
                inline = False
            )
            await bot.get_user(botSettings["creator"]).send(embed=embed)
        await session.close()

@bot.event
async def on_message(message):
    if message.guild and not message.author.bot:
        with bot.sqlConnection.cursor() as cur:
            cur.execute(f"SELECT * FROM serverList WHERE id = '{message.guild.id}';")
            guildSettings = cur.fetchone()
            if guildSettings:
                if guildSettings[1]:
                    if libs.censorshipCheck.check(message):
                        await message.delete()
                        await reply(message, guildSettings[2])
                    else:
                        await bot.process_commands(message)
                else:
                    await bot.process_commands(message)
            else:
                cur.execute("INSERT INTO serverList VALUES (%s, %s, %s, %s);", (str(message.channel.guild.id), False, "Please keep it clean! :underage:", "0"))

#----------Connect to Database----------#

bot.sqlConnection = psycopg2.connect(environ["DATABASE_URL"])
bot.sqlConnection.autocommit = True

#----------Run Bot----------#

if __name__ == "__main__":
    for i in myExtensions:
        try:
            bot.load_extension(i)
        except Exception as error:
            print(f"{i} cannot be loaded.\n{error}")
    bot.run(environ["BOT_TOKEN"])
