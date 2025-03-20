from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    main = State()
    sub_menu = State()
    