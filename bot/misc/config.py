from abc import ABC
from typing import Final


class Config(ABC):
    APP_NAME: Final = 'CHILLVOICE'
    APP_VERSION: Final = '1.0.3'
    APP_LANG: Final = 'ru'
    
    CMD_PREFIX: Final = '!'
    PRESENCE_URL: Final = 'https://twitch.tv/k3ksoff'
    
    ADMIN_ROLE: Final = 1263921519130574898
    
    INTERACTION_TIMEOUT: Final = 15
    
    GUILD_ID: Final = 1263379886039367787
        
    VOICE_CATEGORY: Final = 1263927485725409375
    VOICE_TEXT_CHANNEL: Final = 1263927563571695648
    VOICE_CREATE_CHANNEL: Final = 1264129743779921921
    
    VOICE_CHANNEL_MAX_SLOTS: Final = 99
    VOICE_CHANNEL_MIN_SLOTS: Final = 0
    
    VOICE_CHANNEL_NAME_MIN_LENGTH: Final = 3
    VOICE_CHANNEL_NAME_MAX_LENGTH: Final = 100