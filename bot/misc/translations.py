from abc import ABC
from typing import Final
from .config import Config


class Translations(ABC):
    Lang: Final = Config.APP_LANG
    
    Emojis: Final = {
        "voice_plus": "<:voice_plus:1264091782556155957>",
        "voice_change_slots": "<:voice_change_slots:1264155060279967745>",
        "voice_unlock": "<:voice_unlock:1264157473724694559>",
        "voice_add": "<:voice_add:1264158913008242740>",
        "voice_visible": "<:voice_visible:1264157475188375597>",
        "voice_minus": "<:voice_minus:1264092340557971519>",
        "voice_change_name": "<:voice_change_name:1264155480444637306>",
        "voice_lock": "<:voice_lock:1264157472554225768>",
        "voice_ban": "<:voice_ban:1264158914992144405>",
        "voice_hide": "<:voice_hide:1264157471136677938>",
        "success": "<:success:1265888828472819862>",
        "error": "<:error:1265888826782515272>"
    }
    
    Phrases = {
        "embed_footer": {
            "ru": "discord.gg/chillsquad",
            "en": "discord.gg/chillsquad"
        },
        
        "successful": {
            "ru": "Успешно",
            "en": "Successful"    
        },
        
        # Voice manager embed
        "voice_manager_title": {
            "ru": "**Управление приватной комнатой**",
            "en": "**Voice manager**"
        },
        
        "voice_manager_first_field": {
            "ru": f"""
                {Emojis['voice_plus']} • Добавить 1 слот
                {Emojis['voice_change_slots']} • Изменить слоты
                {Emojis['voice_unlock']} • Открыть канал
                {Emojis['voice_add']} • Добавить пользователя
                {Emojis['voice_visible']} • Показать канал
                ㅤ
            """,
            "en": f"""
                {Emojis['voice_plus']} • Add 1 slot
                {Emojis['voice_change_slots']} • Change slots
                {Emojis['voice_unlock']} • Unlock channel
                {Emojis['voice_add']} • Add user
                {Emojis['voice_visible']} • Show channel
                ㅤ
            """,
        },
        
        "voice_manager_second_field": {
            "ru": f"""
                {Emojis['voice_minus']} • Убрать 1 слот
                {Emojis['voice_change_name']} • Сменить название
                {Emojis['voice_lock']} • Закрыть канал
                {Emojis['voice_ban']} • Заблокировать пользователя
                {Emojis['voice_hide']} • Скрыть канал
                ㅤ
            """,
            "en": f"""
                {Emojis['voice_minus']} • Remove 1 slot
                {Emojis['voice_change_name']} • Change name
                {Emojis['voice_lock']} • Lock channel
                {Emojis['voice_ban']} • Ban user
                {Emojis['voice_hide']} • Hide channel
                ㅤ
            """,
        },
        
        # Interaction errors
        "interaction_error_title": {
            "ru": "Ошибка взаимодействия",
            "en": "Interaction error"
        },
        
        "interaction_error_timeout_title": {
            "ru": "Время ожидания истекло",
            "en": "Timeout expired"
        },
        
        "interaction_error_unknown_description": {
            "ru": "При выполнении команды произошла ошибка. Попробуйте ещё раз\n\nВозможно, стоит обратиться к администрации",
            "en": "An error occurred while executing the command. Try again\n\nIt may be necessary to contact the administrator"    
        },
        
        "interaction_error_timeout_description": {
            "ru": "Время ожидания на команду истекло. Попробуйте ещё раз",
            "en": "The command timeout has expired. Try again"    
        },
        
        "interaction_error_user_no_voice_description": {
            "ru": "Вы должны находиться в голосовом канале",
            "en": "You must be in the voice channel"
        },
        
        "interaction_error_cooldown_description": {
            "ru": "Эта команда сейчас недоступна. Попробуйте ещё раз через {seconds} секунд",
            "en": "This command is currently unavailable. Try again in {seconds} seconds"
        },
        
        "interaction_error_no_permission_description": {
            "ru": "У вас недостаточно прав для выполнения этой команды. Вы должны быть владельцем канала",
            "en": "You do not have permissions to execute this command. You must be the channel owner"
        },
        
        "interaction_error_slots_max_limit_description": {
            "ru": "Вы не можете добавлять больше {slots} участников в голосовой канал",
            "en": "You cannot add more than {slots} members to the voice channel"
        },
        
        "interaction_error_slots_min_limit_description": {
            "ru": "Вы не можете удалять меньше {slots} участников в голосовой канал",
            "en": "You cannot remove less than {slots} members from the voice channel"
        },
        
        # Voice Change Quality
        "select_menu_voice_change_quality_placeholder": {
            "ru": "Изменить качество звука",
            "en": "Change voice quality"    
        },
        
        "select_item_quality_low_label": {
            "ru": "Низкое",
            "en": "Low"
        },
        
        "select_item_quality_economy_label": {
            "ru": "Экономное",
            "en": "Economy"
        },
        
        "select_item_quality_standard_label": {
            "ru": "Стандартное",
            "en": "Standard"
        },
        
        "select_item_quality_high_label": {
            "ru": "Высокое",
            "en": "High"
        },
        
        "select_item_quality_low_description": {
            "ru": "16 кбит/сек",
            "en": "16 kbps"
        },
        
        "select_item_quality_economy_description": {
            "ru": "32 кбит/сек",
            "en": "32 kbps"
        },
        
        "select_item_quality_standard_description": {
            "ru": "64 кбит/сек",
            "en": "64 kbps"
        },
        
        "select_item_quality_high_description": {
            "ru": "96 кбит/сек",
            "en": "96 kbps"
        },
        
        "voice_change_quality_successful_description": {
            "ru": "Вы изменили качество звука на **{quality}**",
            "en": "You changed the voice quality to **{quality}**"    
        },
        
        # Voice Change Slots
        "voice_slots_change_title": {
            "ru": "Изменить количество слотов",
            "en": "Change number of slots"
        },
        
        "voice_slots_change_description": {
            "ru": """
                Укажите количество слотов для голосового канала
                
                **Ограничения:**
                > Максимальное значение: {max_slots}
                > Минимальное значение: {min_slots}
                > 0 = неограничено
                
                Время ожидания: {timeout} секунд
            """,
            "en": """
                Specify the number of slots for the voice channel
                
                **Restrictions:**
                > Maximum value: {max_slots}
                > Minimum value: {min_slots}
                > 0 = unlimited
                
                Waiting time: {timeout} seconds
            """ 
        },
        
        "voice_slot_add_successful_description": {
            "ru": "Вы успешно добавили один слот в голосовой канал",
            "en": "You successfully added one slot to the voice channel"
        },
        
        "voice_slot_remove_successful_description": {
            "ru": "Вы успешно удалили один слот из голосового канала",
            "en": "You successfully removed one slot from the voice channel"
        },
        
        "voice_slots_change_successful_description": {
            "ru": "Вы изменили кол-во слотов на **{slots}**",
            "en": "You changed the voice slots to **{slots}**"
        },
        
        # Voice Unlock
        "voice_unlock_successful_description": {
            "ru": "Вы успешно разблокировали голосовой канал",
            "en": "You unlocked the voice channel"
        },
        
        # Voice Add Members
        "voice_add_member_title": {
            "ru": "Укажите пользователя для добавления",
            "en": "Specify the user to add"
        },
        
        "voice_add_member_description": {
            "ru": """
                Для добавления пользователя в голосовой канал нужно упомянуть его 
                
                (Пример: {example_mention})
                
                Время ожидания: {timeout} секунд
            """,
            "en": """
                To add a user to the voice channel you need to mention them
                
                (Example: {example_mention})
                
                Waiting time: {timeout} seconds
            """
        },
        
        "voice_add_member_successful_description": {
            "ru": "Вы успешно добавили {user} в голосовой канал",
            "en": "You successfully added {user} to the voice channel"
        },
        
        # Voice Visible
        "voice_visible_successful_description": {
            "ru": "Вы успешно сделали голосовой канал видимым",
            "en": "You successfully made the voice channel visible"
        },
        
        # Voice Name Change
        "voice_name_change_title": {
            "ru": "Изменение названия",
            "en": "Change name"
        },
        
        "voice_name_change_description": {
            "ru": """
                Укажите новое название для голосового канала
                
                **Ограничения:**
                > Не менее {min_length} символов
                > Не более {max_length} символов
                > Без специальных знаков
                
                Время ожидания: {timeout} секунд
            """,
            "en": """
                Specify the new name for the voice channel
                
                **Restrictions:**
                > At least {min_length} characters
                > At most {max_length} characters
                > Without special characters
                
                Waiting time: {timeout} seconds
            """
        },
        
        "voice_name_change_successful_description": {
            "ru": "Вы успешно изменили название голосового канала на **{name}**",
            "en": "You successfully changed the voice channel name to **{name}**"
        },
        
        # Voice Lock
        "voice_lock_successful_description": {
            "ru": "Вы успешно заблокировали голосовой канал",
            "en": "You successfully locked the voice channel"
        },
        
        # Voice Ban Members
        "voice_ban_member_title": {
            "ru": "Укажите пользователя для бана",
            "en": "Specify the user to ban"
        },
        
        "voice_ban_member_description": {
            "ru": """
                Для бана пользователя в голосовой канал нужно упомянуть его 
                
                (Пример: {example_mention})
                
                Время ожидания: {timeout} секунд
            """,
            "en": """
                To ban a user from the voice channel you need to mention them
                
                (Example: {example_mention})
                
                Waiting time: {timeout} seconds
            """
        },
        
        "voice_ban_member_successful_description": {
            "ru": "Вы успешно забанили {user} в голосовом канале",
            "en": "You successfully banned {user} from the voice channel"
        },
        
        # Voice Hide
        "voice_hide_successful_description": {
            "ru": "Вы успешно скрыли голосовой канал",
            "en": "You successfully hidden the voice channel"
        }
    }
    
    @staticmethod
    def get_phrase(phrase: str) -> str:
        return Translations.Phrases[phrase][Translations.Lang]
    
    @staticmethod
    def get_emoji(emoji: str) -> str:
        return Translations.Emojis[emoji]