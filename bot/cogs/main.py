from discord.ext.commands import Bot

from bot.cogs.other import register_other_cogs
from bot.cogs.user import register_user_cogs

import asyncio

def register_all_cogs(bot: Bot) -> None:
    cogs = (
        register_user_cogs,
        register_other_cogs,
    )
    for cog in cogs:
        asyncio.run(cog(bot))
