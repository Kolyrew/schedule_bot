from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton

#Main menu ReplyMarkup

main_menu_kb=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="Показать расписание")
                ]
            ]
        )
