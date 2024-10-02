from data import config
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.inline import confirm_admin
from keyboards.keyboard import main_markup, admin_markup
from states import create_states, del_states
from loader import db
from filters import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())

@admin_router.message(Command("create"))
@admin_router.message(F.text == config.cr_test)
async def create_test(message: types.Message, state: FSMContext):
    alr = db.fetchone("SELECT correct FROM current")
    if alr is None:
        await message.answer("Send the correct answers in this format:\n\t<code>4 abcabc...</code>\n\nP.S. - 4 means four options", reply_markup=main_markup)
        await state.set_state(create_states.correct_answer)
    else:
        await message.answer("Delete the current one first")

@admin_router.message(create_states.correct_answer)
async def rec_correct_answer(message: types.Message, state: FSMContext):
    raw = message.text.lower()
    try:
        option = int(raw.split()[0])
    except Exception as e:
        print(e)
        await message.answer("Please, follow the format.")
        await state.clear()
        return
    raw = raw.split()[1]
    num = len(raw)
    legit = True
    for i in raw:
        if i not in "abcdefghijklmnopqrstuvwxyz"[:option]:
            legit = False
            break
    if legit:
        response = f"Can you confirm the test has {num} answers and they are as follows:\n"
        for i in range(num):
            response += f"{i+1}.{raw[i].upper()}"
            if i != num-1:
                response += ", "
        await message.reply(response, reply_markup=confirm_admin)
        await state.update_data(corr=raw)
        await state.update_data(option=option)
        await state.set_state(create_states.confirm)
    else:
        await message.answer("The answer include an option that's not legit")

@admin_router.callback_query(create_states.confirm)
async def create_confirm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "admin_confirm":
        data = await state.get_data()
        corr = data["corr"]
        option = data["option"]
        db.query("INSERT INTO current(correct, option) VALUES (?, ?)", (corr,option))
        await callback.message.answer("Test created")
        await callback.answer("Confirmed")
    elif callback.data == "admin_cancel":
        await callback.message.answer("Test creation cancelled")
        await callback.answer("Cancelled")
    await callback.bot.send_message(callback.message.chat.id, "You've been brought to 🏠 Main menu.", reply_markup=admin_markup)
    await callback.message.delete()
    await state.clear()

@admin_router.message(Command("answers"))
@admin_router.message(F.text == config.shw_ans)
async def shw_answer(message: types.Message, state: FSMContext):
    ans = db.fetchone("SELECT correct FROM current")
    if ans is not None:
        ans=ans[0]
        response = f"The test has {len(ans)} questions. The correct answers are as follows:\n"
        for i in range(len(ans)):
            response += f"{i+1}. {ans[i].upper()}"
            if i != len(ans) - 1:
                response += ", "
        await message.answer(response)
    else:
        await message.answer("There is no test active right now. Create one first")

@admin_router.message(Command("del"))
@admin_router.message(F.text == config.dl_test)
async def delete_test(message: types.Message, state: FSMContext):
    alr = db.fetchone("SELECT correct FROM current")
    if alr is not None:
        await message.answer("Can you confirm you want to delete the test", reply_markup=confirm_admin)
        await state.set_state(del_states.confirm)
        db.create_tables()
    else:
        await message.answer("There is no test active right now. Create one first")

@admin_router.callback_query(del_states.confirm)
async def delete_confirm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "admin_confirm":
        db.query("DELETE FROM current")
        db.query("DELETE FROM user")
        await callback.message.answer("Test deleted")
        await callback.answer("Confirmed")
        await state.clear()
    elif callback.data == "admin_cancel":
        await callback.message.answer("Test deletion cancelled. You can resend the right answers.")
        await callback.answer("Cancelled")
    await callback.message.delete()

@admin_router.message(Command("results"))
@admin_router.message(F.text == config.nm_ans)
async def nm_answer(message: types.Message):
    alr = db.fetchone("SELECT correct FROM current")
    if alr is not None:
        raw = db.fetchall("SELECT idx, fullname, answered FROM user ORDER BY answered DESC")
        if len(raw) > 0:
            response = "The results of the test is as follows:\n"
            for i in range(len(raw)):
                response += f"{i + 1}. {raw[i][1]} - {raw[i][2]}\n"
            await message.answer(response)
        else:
            await message.answer("No one has answered yet")
    else:
        await message.answer("There is no test active right now. Create one first")

def register_admin_handlers(dp):
    dp.include_router(admin_router)