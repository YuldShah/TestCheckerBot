from aiogram import types
from data.config import cancel, confirm

btn = [
    [
        types.InlineKeyboardButton(text=cancel, callback_data="admin_cancel"),
        types.InlineKeyboardButton(text=confirm, callback_data="admin_confirm"),
    ]
]
confirm_admin = types.InlineKeyboardMarkup(inline_keyboard=btn)