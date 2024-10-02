import logging
import sys
from loader import dp, db, bot
from aiogram import types
import asyncio
from data import config
from aiogram.filters import CommandStart
from aiogram import F
from handlers.admin import register_admin_handlers
from handlers.user import register_user_handlers
from keyboards.keyboard import admin_markup, user_markup
from aiogram.fsm.context import FSMContext

@dp.message(CommandStart())
@dp.message(F.text == config.main_menu)
async def process_command(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    response = f"👋 Welcome, <b>{message.from_user.first_name}</b> to the 🏠 Main menu!\n📝 You can /check your answers for the test with this bot."
    markup = user_markup
    if message.from_user.id == config.ADMIN_ID:
        markup = admin_markup
        response = f"👋 Welcome, <b>{message.from_user.first_name}</b> to the 🏠 Main menu!\nYou can:\n\t/create - Create a new test\n\t/results - See the results\n\t/answers - Look at the answers\n\t/del - Delete the test"
    await message.answer(text=response, reply_markup=markup)

async def on_startup():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    db.create_tables()
    logging.warning("Database started...")

async def on_shutdown():
    logging.warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")

async def main():
    await on_startup()
    register_admin_handlers(dp)
    register_user_handlers(dp)
    await dp.start_polling(bot)
    await on_shutdown()



if __name__ == '__main__':
    asyncio.run(main())