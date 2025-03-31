import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent
from dialogs import start_menu, create_task, users_tasks

from config import settings
import base_handlers
from keyboards_menu import set_menu_button
from aiogram_dialog import setup_dialogs

logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s")

    logger.info("Starting bot")

    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.startup.register(set_menu_button)
    dp.errors.register(
        base_handlers.on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.include_router(base_handlers.router)
    dp.include_routers(
        start_menu.start_menu_dialog,
        create_task.task_creation_dialog,
        users_tasks.user_tasks_dialog,
    )
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
