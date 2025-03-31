import logging
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
import fsm_states
import text_templates

router = Router()


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=fsm_states.StartMenu.MAIN, mode=StartMode.RESET_STACK)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=text_templates.HELP_CMD)


async def on_unknown_intent(event, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        fsm_states.StartMenu.MAIN, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND,
    )
