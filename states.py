from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):

    #Начало работы
    START = State()

    #Главное меню
    #(по сути совпадает с началом работы)
    MAIN_MENU = State()

    #Главное меню -> "Показать расписание"
    WAITING_GROUP_NUMBER = State()
    WAITING_PERIOD_SELECTION = State()
    SHOW_SCHEDULE = State()
