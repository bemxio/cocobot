from discord.ext import commands
from discord import Intents
import assets.config as cf
import credentials
import logging

intents = Intents.all()

# logging
logging.basicConfig(
    filename = "discord.log", 
    level = logging.INFO,

    format = "%(levelname)s (%(asctime)s): %(message)s",
    datefmt = "%m/%d/%y %H:%M:%S"
)

bot = commands.Bot(
    command_prefix = cf.prefix, 
    help_command = None, 
    case_insensitive = True,
    intents=intents
)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandNotFound):
        return
    
    if isinstance(err, commands.BotMissingPermissions):
        return await ctx.message.reply(cf.missingperms)
    if isinstance(err, commands.UserInputError):
        return await ctx.message.reply(cf.userinputerror)

    print(err)
    await ctx.message.reply(cf.unexpected.format(err))

# loading extensions
bot.load_extension("extensions.chatter")
bot.load_extension("extensions.debug")
bot.load_extension("extensions.fun")
bot.load_extension("extensions.help")
bot.load_extension("extensions.count")

bot.run(credentials.discord_token)