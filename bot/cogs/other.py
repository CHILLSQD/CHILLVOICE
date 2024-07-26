import discord
from discord.ext.commands import Bot, Cog

from loguru import logger

from bot.misc.config import Config

class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f'Cog has started to load... (cog: {self.__cog_name__}; bot: {self.bot.user.id})')
        
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Streaming(name=Config.APP_NAME, url=Config.PRESENCE_URL))

    
async def register_other_cogs(bot: Bot) -> None:
    await bot.add_cog(__MainOtherCog(bot))
