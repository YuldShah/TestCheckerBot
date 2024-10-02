from data.config import cr_test, dl_test, shw_ans, main_menu, nm_ans
from aiogram import types

btn = [
    [
        types.KeyboardButton(text=cr_test)
    ],
    [
        types.KeyboardButton(text=nm_ans),
        types.KeyboardButton(text=shw_ans)

    ],
    [
        types.KeyboardButton(text=dl_test)
    ]
]

admin_markup = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)

btn1 = [
    [
        types.KeyboardButton(text=main_menu)
    ]
]
main_markup = types.ReplyKeyboardMarkup(keyboard=btn1, resize_keyboard=True)