import logging
import sys
from loader import dp, db, bot, get_info
from aiogram import types
import asyncio
from data import config
from aiogram.filters import CommandStart, Command
from aiogram import F
from handlers.admin import register_admin_handlers
from handlers.user import register_user_handlers
from keyboards.keyboard import admin_markup, user_markup
from aiogram.fsm.context import FSMContext
from handlers.user.check_answers import check_code

from states import check_states


@dp.message(CommandStart())
@dp.message(F.text == config.main_menu)
async def process_command(message: types.Message, state: FSMContext) -> None:
    # referral format of test
    reged = db.fetchone("SELECT COUNT(*) FROM user WHERE userid = ?", (message.from_user.id,))[0] > 0
    if not reged:
        db.query("INSERT INTO user (userid, fullname, username, regdate) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (message.from_user.id, message.from_user.full_name, message.from_user.username))
    todel = ""
    code_mode = False
    if "code" in message.text:
        res = await check_code(message, state)
        if res: return
        else:
            todel = await message.answer("You are being redirected to 🏠 Main menu.")
            from time import sleep
            code_mode = True
            sleep(2)
    await state.clear()
    response = f"👋 Welcome, <b>{message.from_user.first_name}</b> to the 🏠 Main menu!\n📝 You can /check your answers for the test with this bot."
    markup = user_markup
    if message.from_user.id in config.ADMINS:
        markup = admin_markup
        response = f"👋 Welcome, <b>{message.from_user.first_name}</b> to the 🏠 Main menu!"
    await message.answer(text=response, reply_markup=markup)
    if code_mode:
        await todel.delete()

@dp.message(Command("help"))
@dp.message(F.text == config.help_txt)
async def sos(message: types.Message, state: FSMContext) -> None:
    if message.from_user.id in config.ADMINS:
        response = "You can:\n\t/create - Create a new test\n\t/running - See the running tests\n\t/archive - Look at the archive\n\t/stats - See the stats\n\nThe format to follow while sending answers at once:\n<code>first answer\nsecond answer\nthird answer\n...</code>\n\nCredits:\nBy @YuldShah\nSource code - https://github.com/YuldShah/TestCheckerBot"
        await message.answer(response, disable_web_page_preview=True)
    else:
        response = "You can:\n\t/check - Check your answers for a test\n/results - Check your results over the tests\n\nThe format to follow while sending answers at once:\n<code>first answer\nsecond answer\nthird answer\n...</code>"
        await message.answer(response)

async def on_startup():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await get_info(bot)
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
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await on_shutdown()



if __name__ == '__main__':
    asyncio.run(main())