from data.config import cr_test, dl_test, shw_ans, check_ans, results, help_txt
from aiogram import types

btn = [
    [
        types.KeyboardButton(text=check_ans),
        types.KeyboardButton(text=results)
    ],
    [
        types.KeyboardButton(text=help_txt)
    ]
]

user_markup = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)