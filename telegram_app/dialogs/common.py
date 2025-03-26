from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const
import fsm_states

MAIN_MENU_BUTTON = Start(
    text=Const("☰ В главное меню"),
    id="__main__",
    state=fsm_states.StartMenu.MAIN,
)
