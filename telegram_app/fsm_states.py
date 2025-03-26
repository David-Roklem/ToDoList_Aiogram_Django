from aiogram.fsm.state import State, StatesGroup


class StartMenu(StatesGroup):
    MAIN = State()


class TaskCreation(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    category = State()
    result = State()


class UserTasks(StatesGroup):
    MAIN = State()
    specific = State()
