import asyncio
import logging
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent, UnknownState
from dialogs import start_menu, create_task, users_tasks

from config import bot, dp
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

    dp.startup.register(set_menu_button)
    dp.errors.register(
        base_handlers.on_errors,
        ExceptionTypeFilter(UnknownIntent, OutdatedIntent, UnknownState),
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
