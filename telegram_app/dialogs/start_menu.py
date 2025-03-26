from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery
from fsm_states import UserTasks, TaskCreation, StartMenu
import text_templates


async def to_user_tasks(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["user_tasks"] = button.widget_id
    await dialog_manager.start(state=UserTasks.MAIN)


async def to_task_creation(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["task_creation"] = button.widget_id
    await dialog_manager.start(state=TaskCreation.title)


start_menu_dialog = Dialog(
    Window(
        Const(text_templates.START_MENU_TEXT),
        Row(
            Button(
                text=Const(text_templates.USER_TASKS_TEXT),
                id="user_tasks",
                on_click=to_user_tasks,
            ),
            Button(
                text=Const(text_templates.TASK_CREATION_TEXT),
                id="task_creation",
                on_click=to_task_creation,
            ),
        ),
        state=StartMenu.MAIN,
    ),
)
