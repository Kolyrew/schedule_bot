import time
import datetime
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from config import TOKEN_API, urls, driver_path
from processing import get_button, markup_other_info # HIER
from keyboard import main_menu_kb
from messages import main_menu_msg, error_group_number_msg, \
    request_for_group_number, request_for_selection_period, \
    error_datetime_msg, error_datetime_existing_msg
#from states import States
from database import start_work, check_user_id, get_group_number, \
    insert_user_id
from parser import get_schedule

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

# Инициализация бота
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    start_work()
    await States.MAIN_MENU.set()
    await message.answer(main_menu_msg, parse_mode="HTML", reply_markup=main_menu_kb)

@dp.message_handler(text="Показать расписание", state=States.MAIN_MENU)
async def btn_clk_show_schedule(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if not check_user_id(user_id=message.chat.id):
        await message.answer(request_for_group_number, parse_mode="HTML")
        await States.WAITING_GROUP_NUMBER.set()
    else:
        await message.answer(request_for_selection_period, parse_mode="HTML")
        await States.WAITING_PERIOD_SELECTION.set()


@dp.message_handler(state=States.WAITING_GROUP_NUMBER)
async def got_group_number(message : types.Message, state: FSMContext):
    if check_user_id(user_id=message.chat.id):
        group_number = get_group_number(message.chat.id)
    else:
        group_number = message.text
        insert_user_id(message.chat.id, group_number)
    await States.WAITING_PERIOD_SELECTION.set()
    await message.answer(request_for_selection_period, parse_mode="HTML")
    await got_selection_period(message, state, group_number)

# Эти две функции объединены в одну ниже.
# Соответственно, если работает, нужно удалить старое состояние.


"""
@dp.message_handler(state=States.WAITING_PERIOD_SELECTION)
async def got_selection_period(message: types.Message, state: FSMContext): # HIER
    group_number = get_group_number(message.chat.id)
    formatted_period = None
    try:
        period = list(map(int, message.text.replace(" ", "").split(".")))
    except Exception as e:
        await bot.send_message(error_datetime_msg, parse_mode="HTML")
        formatted_period = datetime.now()
    try:
        if len(period) == 3: formatted_period = datetime(period[2], period[1], period[0], 0, 0, 0)
        elif len(period) == 2: formatted_period = datetime(datetime.now().year, period[1], period[0], 0, 0, 0)
        elif len(period) == 1: formatted_period = datetime(datetime.now().year, datetime.now().month, period[0], 0, 0, 0)
        else:
            await bot.send_message(error_datetime_msg, parse_mode="HTML")
            formatted_period = datetime.now()
    except Exception as e:
        await bot.send_message(error_datetime_msg, parse_mode="HTML")
        formatted_period = datetime.now()
    await States.SHOW_SCHEDULE.set()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await got_schedule(state, formatted_period)


@dp.message_handler(state=States.SHOW_SCHEDULE)
async def got_schedule(state: FSMContext, date):
    group_number = get_group_number(message.chat.id)

    flag = None
    if date > datetime.now(): flag = "Later"
    elif date < datetime.now(): flag = "Earlier"
    elif date == datetime.now(): flag = "Today"
    else:
        bot.send_message(error_datetime_existing_msg)
        date = datetime.now()
        flag = "Today"
    day_text = get_schedule(flag, date, group_number)
    await bot.send_message(day_text, parse_mode="HTML")
    await States.MAIN_MENU.set()
"""

@dp.message_handler(state=States.WAITING_PERIOD_SELECTION)
async def got_selection_period(message: types.Message, state: FSMContext):
    group_number = get_group_number(message.chat.id)
    formatted_period = None
    try:
        period = list(map(int, message.text.replace(" ", "").split(".")))
        if len(period) == 3:
            formatted_period = datetime(period[2], period[1], period[0], 0, 0, 0)
        elif len(period) == 2:
            formatted_period = datetime(datetime.now().year, period[1], period[0], 0, 0, 0)
        elif len(period) == 1:
            formatted_period = datetime(datetime.now().year, datetime.now().month, period[0], 0, 0, 0)
        else:
            await bot.send_message(error_datetime_msg, parse_mode="HTML")
            formatted_period = datetime.now()
    except Exception as e:
        await bot.send_message(error_datetime_msg, parse_mode="HTML")
        formatted_period = datetime.now()
    await States.SHOW_SCHEDULE.set()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    date = formatted_period
    flag = None
    if date > datetime.now():
        flag = "Later"
    elif date < datetime.now():
        flag = "Earlier"
    elif date == datetime.now():
        flag = "Today"
    else:
        bot.send_message(error_datetime_existing_msg)
        date = datetime.now()
        flag = "Today"
    day_text = get_schedule(flag, date, group_number)
    await bot.send_message(day_text, parse_mode="HTML")
    await States.MAIN_MENU.set()



if __name__ == "__main__":
    executor.start_polling(dp)
