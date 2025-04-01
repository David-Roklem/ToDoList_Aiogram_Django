from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import (
    Dialog,
    DialogManager,
    Window,
    StartMode,
)
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Next, Back, Select, Group, Button
from aiogram_dialog.widgets.text import Const, Jinja, Format
import httpx
from dialogs.common import MAIN_MENU_BUTTON
from utils import extract_elements, title_check
import text_templates
from fsm_states import TaskCreation, StartMenu
from config import settings


async def get_actual_categories(dialog_manager: DialogManager, **kwargs):
    base_url = settings.BACKEND_SERVER_ADDRESS
    data = httpx.get(f"{base_url}categories/")
    return {"categories": data.json()}


async def save_title_data(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, title):
    dialog_manager.dialog_data["title"] = title
    await dialog_manager.switch_to(TaskCreation.description)


async def save_description_data(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, description):
    dialog_manager.dialog_data["description"] = description
    await dialog_manager.switch_to(TaskCreation.due_date)


async def save_due_date_data(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, due_date):
    dialog_manager.dialog_data["due_date"] = due_date
    await dialog_manager.switch_to(TaskCreation.category)


async def save_category_data(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, category):
    category_name, category = extract_elements(category)
    dialog_manager.dialog_data["category_name"] = category_name
    dialog_manager.dialog_data["category"] = category
    await dialog_manager.switch_to(TaskCreation.result)


async def error_title_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(text="Вы ввели некорректное название задачи. Попробуйте еще раз")


def due_date_check(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        return date_string
    except ValueError:
        raise ValueError


async def error_due_date_handler(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.answer(text="Вы указали дату в некорректном формате. Попробуйте еще раз")


async def created_task_getter(dialog_manager: DialogManager, **kwargs):
    description = dialog_manager.dialog_data.get("description", "")
    return {
        "title": dialog_manager.dialog_data["title"],
        "description": description,
        "category": dialog_manager.dialog_data.get("category_name"),
        "due_date": dialog_manager.dialog_data["due_date"],
    }


def check_if_user_exists(dialog_manager: DialogManager):
    # TODO Закэшировать логику проверки юзера в БД
    base_url = settings.BACKEND_SERVER_ADDRESS
    telegram_id = dialog_manager.event.from_user.id
    user = httpx.get(f"{base_url}users/user-detail/{telegram_id}")
    return True if user.status_code == 200 else False


async def create_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    base_url = settings.BACKEND_SERVER_ADDRESS
    user_id = dialog_manager.event.from_user.id
    full_name = dialog_manager.event.from_user.full_name
    data = dialog_manager.dialog_data
    data["user"] = user_id
    if not check_if_user_exists(dialog_manager):
        httpx.post(f"{base_url}users/create", json={"telegram_id": user_id, "name": full_name})
    httpx.post(f"{base_url}user-tasks/create", json=data)
    await dialog_manager.done()
    await callback.answer(text_templates.TASK_CREATED_TEXT, show_alert=True)


task_creation_dialog = Dialog(
    Window(
        Const(text_templates.ADD_TITLE_TEXT),
        TextInput(
            id="title",
            type_factory=title_check,
            on_error=error_title_handler,
            on_success=save_title_data,
        ),
        MAIN_MENU_BUTTON,
        state=TaskCreation.title,
    ),
    Window(
        Const(text_templates.ADD_DESC_TEXT),
        TextInput(id="description", on_success=save_description_data),
        MAIN_MENU_BUTTON,
        Back(Const("Назад")),
        Next(Const("Пропустить")),
        state=TaskCreation.description,
    ),
    Window(
        Const(text_templates.ADD_DUE_DATE_TEXT),
        TextInput(
            id="due_date",
            type_factory=due_date_check,
            on_error=error_due_date_handler,
            on_success=save_due_date_data,
        ),
        MAIN_MENU_BUTTON,
        Back(Const("Назад")),
        state=TaskCreation.due_date,
    ),
    Window(
        Const(text_templates.ADD_CATEGORY_TEXT),
        Group(
            Select(
                Format("{item[name]}"),
                id="category",
                item_id_getter=lambda x: (x["name"], x["id"]),
                items="categories",
                on_click=save_category_data,
            ),
            width=2,
        ),
        MAIN_MENU_BUTTON,
        Back(Const("Назад")),
        state=TaskCreation.category,
        getter=get_actual_categories,
    ),
    Window(
        Jinja(
            "<b>Вы ввели следующие данные</b>:\n\n"
            "<b>Название</b>: {{title}}\n"
            "<b>Описание</b>: {{description}}\n"
            "<b>Категория</b>: {{category}}\n"
            "<b>Дата выполнения</b>: {{due_date}}\n\n"
            "<b>Подтвердить создание задачи?</b>\n"
        ),
        Button(
            Const(text_templates.APPROVE_TASK_CREATION_TEXT),
            id="approve_task_creation",
            on_click=create_task,
        ),
        MAIN_MENU_BUTTON,
        Back(Const("Назад")),
        state=TaskCreation.result,
        getter=created_task_getter,
        parse_mode="html",
    ),
)
