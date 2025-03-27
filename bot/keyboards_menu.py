import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

logger = logging.getLogger(__name__)


async def set_menu_button(bot: Bot):
    menu_commands = [
        BotCommand(command='/start',
                   description='Запустить бота'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
    ]
    await bot.set_my_commands(menu_commands, scope=BotCommandScopeDefault())
