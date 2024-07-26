import logging
from loguru import logger

from bot import start_bot

from bot.misc.config import Config
from bot.misc.path import PathManager

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

if __name__ == '__main__':
    log_path = PathManager.get('logs/debug.log')
    logger.add(
        log_path, 
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}", 
        level="DEBUG", 
        rotation="10:00", 
        compression="zip",
        backtrace=True
    )
    
    discord_logger = logging.getLogger()
    discord_logger.setLevel(logging.INFO)

    handler = InterceptHandler()
    discord_logger.addHandler(handler)
    
    print("\033[92m\n\n")
    print("   ▄█▄     ▄  █ ▄█ █    █       ▄   ████▄ ▄█ ▄█▄    ▄███▄   ")
    print("   █▀ ▀▄  █   █ ██ █    █        █  █   █ ██ █▀ ▀▄  █▀   ▀  ")
    print("   █   ▀  ██▀▀█ ██ █    █   █     █ █   █ ██ █   ▀  ██▄▄    ")
    print("   █▄  ▄▀ █   █ ▐█ ███▄ ███▄ █    █ ▀████ ▐█ █▄  ▄▀ █▄   ▄▀ ")
    print("   ▀███▀     █   ▐     ▀    ▀ █  █         ▐ ▀███▀  ▀███▀   ")
    print("            ▀                  █▐                           ")
    print("                               ▐                            ")
    print(f"\033[94m            {Config.APP_NAME} v{Config.APP_VERSION}")
    print(f"\033[94m     Powered by discord.gg/chillsquad", end='\033[0m\n\n\n\n')
    
    start_bot()
