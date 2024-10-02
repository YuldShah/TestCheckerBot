from pyexpat.errors import messages

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from loader import db
from states import check_states
from data import config
from aiogram.filters import Command
from keyboards.inline import confirm_user

user_router = Router()

@user_router.message(Command("check"))
@user_router.message(F.text == config.check_ans)
async def receive_ans(message: types.Message, state: FSMContext):
    alr = db.fetchone("SELECT correct FROM current")
    if alr is not None:
        answered = db.fetchone("SELECT answered FROM user WHERE idx = ?", (message.from_user.id,))
        if answered is not None:
            answered = int(answered[0])
            await message.answer(f"You have already answered! Your result is\nCorrect answers: {answered} out of {len(alr[0])}\nPercentage: {round(100*answered/len(alr[0]), 2)}%")
        else:
            await message.answer("Send the correct answers in this format:\n\t<code>abcabc...</code>")
            await state.set_state(check_states.receiving)
    else:
        await message.answer("There is no test active right now")

@user_router.message(check_states.receiving)
async def check_answers(message: types.Message, state: FSMContext):
    corr = db.fetchone("SELECT correct FROM current")[0].lower()
    option = int(db.fetchone("SELECT option FROM current")[0])
    await state.update_data(corr=corr)
    raw = message.text.lower()
    num = len(raw)
    legit = len(corr) == num
    for i in raw:
        if i not in "abcdefghijklmnopqrstuvwxyz"[:option]:
            legit = False
            break
    if legit:
        response = f"Can you confirm your answers are as follows:\n"
        for i in range(num):
            response += f"{i+1}.{raw[i].upper()}"
            if i != num-1:
                response += ", "
        await message.reply(response, reply_markup=confirm_user)
        await state.update_data(user_ans=raw)
        await state.set_state(check_states.confirm)
    else:
        await message.answer("The answer include an option that's not legit or the number of answers is not quite right")

@user_router.callback_query(check_states.confirm)
async def confirm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "user_confirm":
        data = await state.get_data()
        corr = data['corr']
        user_ans = data['user_ans']
        num_corr = 0
        for i in range(len(corr)):
            num_corr += corr[i] == user_ans[i]
        db.query("INSERT INTO user(idx, fullname, answered) VALUES (?, ?, ?)", (callback.from_user.id, callback.from_user.full_name, num_corr))
        await callback.message.answer(f"Your result is\nCorrect answers: {num_corr} out of {len(user_ans)}\nPercentage: {round(100*num_corr/len(user_ans), 2)}%")
        await callback.answer("Confirmed")
        await state.clear()
    elif callback.data == "user_cancel":
        await callback.message.answer("The checking has been cancelled. You can resend your answers.")
        await callback.answer("Cancelled")
    await callback.message.delete()


def register_user_handlers(dp):
    dp.include_router(user_router)