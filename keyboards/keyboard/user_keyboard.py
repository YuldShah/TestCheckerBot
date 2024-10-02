from data.config import cr_test, dl_test, shw_ans, check_ans
from aiogram import types

btn = [
    [
        types.KeyboardButton(text=check_ans)
    ]
]

user_markup = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)