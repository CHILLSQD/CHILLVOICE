import discord
import asyncio

from discord.ext import commands
from discord.ext.commands import Cog, Bot
from discord.ext.tasks import loop

from loguru import logger

from bot.misc.config import Config
from bot.misc.translations import Translations
from bot.misc.util import Embed


class VoiceManagerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            1, 3, commands.BucketType.member
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool: 
        user = interaction.user
        user_avatar_url = user.display_avatar.url

        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            await interaction.response.send_message(ephemeral=True, embed = Embed(
                "interaction_error_title",
                "interaction_error_cooldown_description",
                {"seconds": round(retry_after)},
                thumbnail_url=user_avatar_url
            ))
            return False

        if user.voice is None:
            await interaction.response.send_message(ephemeral=True, embed = Embed(
                "interaction_error_title",
                "interaction_error_user_no_voice_description",
                thumbnail_url=user_avatar_url
            ))
            return False

        if not user.voice.channel.permissions_for(user).manage_channels:
            await interaction.response.send_message(ephemeral=True, embed = Embed(
                "interaction_error_title",
                "interaction_error_no_permission_description",
                thumbnail_url=user_avatar_url
            ))
            return False

        await interaction.response.defer(ephemeral=True)
        return True

    async def on_error(
        self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item
    ) -> None:

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "interaction_error_title",
            "interaction_error_unknown_description",
            thumbnail_url=interaction.user.display_avatar.url
        ))

        logger.opt(exception=error).error(
            f"\nError during interaction ({interaction.id}):\n"
            f"\nUser: {interaction.user.name} ({interaction.user.id})\n"
            f"\nInteraction item: {item}\n"
            f"\nError: {error}"
            f"\n\n"
        )

    @discord.ui.select(
        placeholder=Translations.get_phrase(
            "select_menu_voice_change_quality_placeholder"
        ),
        min_values=1,
        max_values=1,
        custom_id="voice_quality_select",
        options=[
            discord.SelectOption(
                label=Translations.get_phrase("select_item_quality_low_label"),
                description=Translations.get_phrase(
                    "select_item_quality_low_description"
                ),
            ),
            discord.SelectOption(
                label=Translations.get_phrase("select_item_quality_economy_label"),
                description=Translations.get_phrase(
                    "select_item_quality_economy_description"
                ),
            ),
            discord.SelectOption(
                label=Translations.get_phrase("select_item_quality_standard_label"),
                description=Translations.get_phrase(
                    "select_item_quality_standard_description"
                ),
            ),
            discord.SelectOption(
                label=Translations.get_phrase("select_item_quality_high_label"),
                description=Translations.get_phrase(
                    "select_item_quality_high_description"
                ),
            ),
        ],
    )
    async def select_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        voice_channel = interaction.user.voice.channel

        bitrate_mapping = {
            Translations.get_phrase("select_item_quality_low_label"): 16000,
            Translations.get_phrase("select_item_quality_economy_label"): 32000,
            Translations.get_phrase("select_item_quality_standard_label"): 64000,
            Translations.get_phrase("select_item_quality_high_label"): 96000,
        }

        bitrate = bitrate_mapping.get(select.values[0], 64000)

        await voice_channel.edit(bitrate=bitrate)

        await interaction.followup.send(ephemeral=True, embed = Embed(
                "successful",
                "voice_change_quality_successful_description",
                {"quality": select.values[0]},
                thumbnail_url=interaction.user.display_avatar.url
        ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_plus"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_slot_add",
    )
    async def voice_slot_add_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_channel = interaction.user.voice.channel
        user_avatar_url = interaction.user.display_avatar.url
        slots = voice_channel.user_limit
        max_slots = Config.VOICE_CHANNEL_MAX_SLOTS

        if slots >= max_slots:
            await interaction.followup.send(ephemeral=True, embed = Embed(
                "interaction_error_title",
                "interaction_error_slots_max_limit_description",
                {"slots": max_slots},
                thumbnail_url=user_avatar_url
            ))
            return

        await voice_channel.edit(user_limit=slots + 1)
        
        await interaction.followup.send(ephemeral=True, embed = Embed(
            "successful",
            "voice_slot_add_successful_description",
            thumbnail_url=user_avatar_url
        ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_change_slots"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_slots_change",
    )
    async def voice_slots_change_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_channel = interaction.user.voice.channel
        slots = voice_channel.user_limit
        user_avatar_url = interaction.user.display_avatar.url

        max_slots = Config.VOICE_CHANNEL_MAX_SLOTS
        min_slots = Config.VOICE_CHANNEL_MIN_SLOTS
        interaction_timeout = Config.INTERACTION_TIMEOUT

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "voice_slots_change_title",
            "voice_slots_change_description",
            {"min_slots": min_slots, "max_slots": max_slots, "timeout": interaction_timeout},
            thumbnail_url=user_avatar_url
        ))

        def check(msg: discord.Message):
            if (
                msg.author == interaction.user and
                msg.channel == interaction.channel and
                msg.author.voice.channel == voice_channel
            ):
                try:
                    slots = int(msg.content)
                    return min_slots <= slots <= max_slots
                except ValueError:
                    pass
            return False

        try:
            message: discord.Message = await interaction.client.wait_for(
                "message", check=check, timeout=interaction_timeout
            )
            
            slots = int(message.content)

            await voice_channel.edit(user_limit = slots)

            await interaction.followup.send(ephemeral=True, embed = Embed(
                "successful",
                "voice_slots_change_successful_description",
                {"slots": slots},
                thumbnail_url=user_avatar_url
            ))
        except asyncio.TimeoutError:
            await interaction.followup.send(ephemeral=True, embed = Embed(
                "interaction_error_timeout_title",
                "interaction_error_timeout_description",
                thumbnail_url=user_avatar_url
            ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_unlock"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_unlock",
    )
    async def voice_unlock_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_channel = interaction.user.voice.channel
        default_role = interaction.guild.default_role

        perms: discord.PermissionOverwrite = voice_channel.overwrites_for(default_role)
        perms.connect = True

        await voice_channel.set_permissions(default_role, overwrite=perms)

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "successful",
            "voice_unlock_successful_description",
            thumbnail_url=interaction.user.display_avatar.url
        ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_add"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_add_member",
    )
    async def voice_add_member_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user_avatar_url = interaction.user.display_avatar.url
        voice_channel = interaction.user.voice.channel
        
        timeout = Config.INTERACTION_TIMEOUT
        
        await interaction.followup.send(ephemeral=True, embed = Embed(
            "voice_add_member_title",
            "voice_add_member_description",
            {"example_mention": interaction.client.user.mention, "timeout": timeout},
            thumbnail_url=user_avatar_url
        ))

        def check(msg: discord.Message):
            return (
                msg.author == interaction.user and
                msg.channel == interaction.channel and
                msg.author.voice.channel == voice_channel and
                len(msg.mentions) == 1 and
                msg.mentions[0] != interaction.user
            )

        try:
            message: discord.Message = await interaction.client.wait_for(
                "message", check=check, timeout=timeout
            )
            
            mention_user = message.mentions[0]

            perms: discord.PermissionOverwrite = voice_channel.overwrites_for(mention_user)
            perms.update(connect=True, view_channel=True, speak=True)

            await voice_channel.set_permissions(mention_user, overwrite=perms)

            await interaction.followup.send(ephemeral=True, embed = Embed(
                "successful",
                "voice_add_member_successful_description",
                {"user": mention_user.mention},
                thumbnail_url=user_avatar_url
            ))
        except asyncio.TimeoutError:
            await interaction.followup.send(ephemeral=True, embed = Embed(
                "interaction_error_timeout_title",
                "interaction_error_timeout_description",
                thumbnail_url=user_avatar_url
            ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_visible"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_visible",
    )
    async def voice_visible_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_channel = interaction.user.voice.channel
        default_role = interaction.guild.default_role

        perms: discord.PermissionOverwrite = voice_channel.overwrites_for(default_role)
        perms.view_channel = True

        await voice_channel.set_permissions(default_role, overwrite=perms)

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "successful",
            "voice_visible_successful_description",
            thumbnail_url=interaction.user.display_avatar.url
        ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_minus"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_slot_remove",
    )
    async def voice_slot_remove_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_channel = interaction.user.voice.channel
        user_avatar_url = interaction.user.display_avatar.url
        slots = interaction.user.voice.channel.user_limit
        min_slots = Config.VOICE_CHANNEL_MIN_SLOTS

        if slots <= min_slots:
            await interaction.followup.send(ephemeral=True, embed = Embed(
                "interaction_error_title",
                "interaction_error_slots_min_limit_description",
                {"slots": min_slots},
                thumbnail_url=user_avatar_url
            ))
            return

        await voice_channel.edit(user_limit=slots - 1)

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "successful",
            "voice_slot_remove_successful_description",
            thumbnail_url=user_avatar_url
        ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_change_name"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_name_change",
    )
    async def voice_name_change_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user = interaction.user
        user_avatar_url = user.display_avatar.url
        voice_channel = user.voice.channel
        
        min_length = Config.VOICE_CHANNEL_NAME_MIN_LENGTH
        max_length = Config.VOICE_CHANNEL_NAME_MAX_LENGTH
        timeout = Config.INTERACTION_TIMEOUT

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "voice_name_change_title",
            "voice_name_change_description",
            {"min_length": min_length, "max_length": max_length, "timeout": timeout},
            thumbnail_url=user_avatar_url
        ))

        def check(msg: discord.Message):
            return (
                msg.author == user and
                msg.channel == interaction.channel and
                msg.author.voice.channel == voice_channel and
                min_length <= len(msg.content) <= max_length
            )

        try:
            message: discord.Message = await interaction.client.wait_for(
                "message", check=check, timeout=timeout
            )
            
            await voice_channel.edit(name=message.content)
            
            await interaction.followup.send(ephemeral=True, embed = Embed(
                "successful",
                "voice_name_change_successful_description",
                {"name": message.content},
                thumbnail_url=user_avatar_url
            ))  
        except asyncio.TimeoutError:
            await interaction.followup.send(ephemeral=True, embed = Embed(
                "interaction_error_timeout_title",
                "interaction_error_timeout_description",
                thumbnail_url=user_avatar_url
            ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_lock"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_lock",
    )
    async def voice_lock_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_channel = interaction.user.voice.channel
        default_role = interaction.guild.default_role

        perms: discord.PermissionOverwrite = voice_channel.overwrites_for(default_role)
        perms.connect = False

        await voice_channel.set_permissions(default_role, overwrite=perms)

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "successful",
            "voice_lock_successful_description",
            thumbnail_url=interaction.user.display_avatar.url
        ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_ban"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_ban_member",
    )
    async def voice_ban_member_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        user = interaction.user
        user_avatar_url = user.display_avatar.url
        voice_channel = user.voice.channel
        
        timeout = Config.INTERACTION_TIMEOUT

        await interaction.followup.send(ephemeral=True, embed = Embed(
            "voice_ban_member_title",
            "voice_ban_member_description",
            {"example_mention": interaction.client.user.mention, "timeout": timeout},
            thumbnail_url=user_avatar_url
        ))

        def check(msg: discord.Message):
            return (
                (msg.author == user)
                and (msg.channel == interaction.channel)
                and (msg.author.voice.channel == voice_channel)
                and (len(msg.mentions) == 1)
                and (msg.mentions[0] != interaction.user)
            )

        try:
            message: discord.Message = await interaction.client.wait_for(
                "message", check=check, timeout=timeout
            )
            
            mention_user = message.mentions[0]

            perms: discord.PermissionOverwrite = voice_channel.overwrites_for(mention_user)
            perms.update(connect=False, view_channel=False, speak=False)

            await voice_channel.set_permissions(mention_user, overwrite=perms)

            await interaction.followup.send(ephemeral=True, embed = Embed(
                "successful",
                "voice_ban_member_successful_description",
                {"user": mention_user.mention},
                thumbnail_url=user_avatar_url
            ))
        except asyncio.TimeoutError:
            await interaction.followup.send(ephemeral=True, embed = Embed(
                "interaction_error_timeout_title",
                "interaction_error_timeout_description",
                thumbnail_url=user_avatar_url
            ))

    @discord.ui.button(
        label="",
        emoji=Translations.get_emoji("voice_hide"),
        style=discord.ButtonStyle.gray,
        custom_id="voice_hide",
    )
    async def voice_hide_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_channel = interaction.user.voice.channel
        default_role = interaction.guild.default_role

        perms: discord.PermissionOverwrite = voice_channel.overwrites_for(default_role)
        perms.view_channel = False

        await voice_channel.set_permissions(default_role, overwrite=perms)
        
        await interaction.followup.send(ephemeral=True, embed = Embed(
            "successful",
            "voice_hide_successful_description",
            thumbnail_url=interaction.user.display_avatar.url
        ))

class __MainUserCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None
        

    async def setup(self) -> None:
        text_channel = self.guild.get_channel(Config.VOICE_TEXT_CHANNEL)

        await text_channel.purge()
        
        embed = Embed("voice_manager_title")
        
        embed.add_field(
            name="ㅤ",
            value=Translations.get_phrase("voice_manager_first_field"),
        )
        embed.add_field(
            name="ㅤ",
            value=Translations.get_phrase("voice_manager_second_field"),
        )

        await text_channel.send(embed=embed, view=VoiceManagerView())

    @loop(minutes=1)
    async def delete_empty_voice(self):
        for voice_channel in self.guild.voice_channels:
            if voice_channel.category_id != Config.VOICE_CATEGORY or voice_channel.id == Config.VOICE_CREATE_CHANNEL:
                continue
            
            if len(voice_channel.members) == 0:
                try:
                    await voice_channel.delete()
                except discord.HTTPException as e:
                    logger.error(
                        f"\nFailed to delete empty voice channel. (delete_empty_voice)\n"
                        f"Channel: {voice_channel.name} ({voice_channel.id})\n"
                        f"Members: {len(voice_channel.members)}\n"
                        f"Error: {e}"
                    )

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info(
            f"Cog has started to load... (cog: {self.__cog_name__}; bot: {self.bot.user.id})"
        )
        
        self.guild = self.bot.get_guild(Config.GUILD_ID)
        self.bot.add_view(VoiceManagerView())
        
        await self.setup()
        await self.delete_empty_voice.start()

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.category_id == Config.VOICE_CATEGORY:
            if message.channel.id == Config.VOICE_TEXT_CHANNEL:
                try:
                    await message.delete(delay=1)
                except discord.HTTPException as e:
                    logger.error(
                        f"\nFailed to delete message. (on_message)\n"
                        f"Channel: {message.channel.name} ({message.channel.id})\n"
                        f"Author: {message.author.name} ({message.author.id})\n"
                        f"Message: {message.content}\n"
                        f"Error: {e}"
                    )
    @Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if before.channel and before.channel.category_id == Config.VOICE_CATEGORY:
            if before.channel.id != Config.VOICE_CREATE_CHANNEL and len(before.channel.members) == 0:
                try:
                    await before.channel.delete()
                except discord.HTTPException as e:
                    logger.error(
                        f"\nFailed to delete empty voice channel. (on_voice_state_update)\n"
                        f"Channel: {before.channel.name} ({before.channel.id})\n"
                        f"Members: {len(before.channel.members)}\n"
                        f"Error: {e}"
                    )

        if after.channel and after.channel.id == Config.VOICE_CREATE_CHANNEL:
        
            new_channel_name = f"{member.name}'s room"
            category = after.channel.category
            
            permissions = {
                member: discord.PermissionOverwrite(
                    view_channel=True,
                    manage_channels=True,
                    connect=True,
                    speak=True,
                    mute_members=True,
                    deafen_members=True,
                    move_members=True
                ),
                self.guild.default_role: discord.PermissionOverwrite(connect=False)
            }
            
            new_channel = await self.guild.create_voice_channel(name=new_channel_name, category=category, overwrites=permissions)
            await member.move_to(new_channel)

async def register_user_cogs(bot: Bot) -> None:
    await bot.add_cog(__MainUserCog(bot))