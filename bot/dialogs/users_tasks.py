from aiogram_dialog.widgets.kbd import Back, Group, Select
from aiogram_dialog.widgets.text import Const, Jinja, Format
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram.types import CallbackQuery
import httpx
from fsm_states import UserTasks
from dialogs.common import MAIN_MENU_BUTTON
import text_templates
from config import settings


async def get_user_tasks(dialog_manager: DialogManager, **kwargs):
    base_url = settings.BACKEND_SERVER_ADDRESS
    user_id = dialog_manager.event.from_user.id
    user_tasks = httpx.get(f"{base_url}user-tasks/{user_id}")
    res = {"user_tasks": user_tasks.json()}
    dialog_manager.dialog_data["user_tasks"] = res["user_tasks"]
    return res


async def task_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: int):
    dialog_manager.dialog_data["requested_task_id"] = item_id
    await dialog_manager.switch_to(state=UserTasks.specific)


async def tasks_data_getter(dialog_manager: DialogManager, **kwargs):
    requested_task_id = dialog_manager.dialog_data.get("requested_task_id")
    user_tasks = dialog_manager.dialog_data["user_tasks"]
    for task in user_tasks:
        if task["id"] == int(requested_task_id):
            description = task["description"]
            if description is None:
                description = ""
            res = {
                "title": task["title"],
                "description": description,
                "category": task["category_name"],
                "created_at": task["created_at"],
                "due_date": task["due_date"],
            }
            return res
    return {}


user_tasks_dialog = Dialog(
    Window(
        Const(text_templates.USER_TASKS_TEXT),
        Group(
            Select(
                Format("{item[title]}"),
                id="task",
                item_id_getter=lambda x: x["id"],
                items="user_tasks",
                on_click=task_selection
            ),
            width=2,
        ),
        MAIN_MENU_BUTTON,
        state=UserTasks.MAIN,
        getter=get_user_tasks,
    ),
    Window(
        Jinja(
            "<b>Название задачи</b>: {{title}}\n"
            "<b>Описание</b>: {{description}}\n"
            "<b>Категория</b>: {{category}}\n"
            "<b>Дата создания</b>: {{created_at}}\n"
            "<b>Дата выполнения</b>: {{due_date}}\n"
        ),
        MAIN_MENU_BUTTON,
        Back(Const("Назад")),
        state=UserTasks.specific,
        getter=tasks_data_getter,
        parse_mode="html",
        # on_process_result=close_dialog,
    ),
)
