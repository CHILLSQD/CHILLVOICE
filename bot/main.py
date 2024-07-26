from discord import Intents
from discord.ext.commands import Bot

from bot.misc import Env, Config
from bot.cogs import register_all_cogs

def start_bot():
    bot = Bot(Config.CMD_PREFIX, intents=Intents.all())
    
    bot.remove_command('help')

    register_all_cogs(bot)
    
    bot.run(Env.TOKEN, log_handler=None)