import discord

from bot.misc.translations import Translations

class Embed(discord.Embed):
    def __init__(self, title_key: str, description_key: str = None, description_format_args = None, thumbnail_url: str = None):
        description = Translations.get_phrase(description_key).format(**(description_format_args or {})) if description_key else None
        
        super().__init__(
            title = Translations.get_phrase(title_key),
            description = description,
            colour = discord.Color.from_rgb(47, 49, 54),
        )
        
        self.set_thumbnail(url=thumbnail_url) if thumbnail_url else None    
        self.set_footer(text=Translations.get_phrase("embed_footer"))
        
        