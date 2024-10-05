from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from filters import UserFilter
from keyboards.keyboard import user_markup, num_quests
from loader import db
from data import config
from states.check_states import results_states

res = Router()
res.message.filter(UserFilter())
res.callback_query.filter(UserFilter())

@res.message(Command("results"))
@res.message(F.text == config.results)
async def shresults(message: Message, state: FSMContext):
    btn = [
        [
            InlineKeyboardButton(text="Last test", callback_data="last"),
        ]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=btn)
    await state.set_state(results_states.choice)
    await message.answer("Choose which test you want to know the results of or enter the code:", reply_markup=markup)

@res.message(results_states.choice)
async def coderesults(message: Message, state: FSMContext):
    code = message.text
    if len(code) != 6:
        await message.answer("Please enter a valid code.", reply_markup=user_markup)
    else:
        exam = db.fetchone("SELECT * FROM exams WHERE code = ?", (code,))
        if exam is not None:

            exid, title, about, total = exam[0], exam[2], exam[3], exam[4]
            # userid = db.fe
            ress = f"<b>Title: </b> {title}"
            ress += f"\n<b>Description: {about}</b>" if about!="__skip" else ""
            ress += f"\n<b>Number of questions: {total}</b>\n"
            corr = db.fetchone("SELECT corr, date FROM submissions WHERE exid = ? AND userid = ?", (exid,message.from_user.id))
            date = corr[1]
            ress += f"\n<b>Submitted: </b>{date} UTC"
            ress += f"\n<b>Correct answers:</b> {corr[0]} out of {total}\n<b>Percentage:</b> {round(100*corr[0]/total, 2)}%"
            running = exam[6]
            if not running:
                await state.update_data(corr=exam[5])
                btn = [
                    [
                        InlineKeyboardButton(text="👁 Reveal the correct answers", callback_data=f"show_ans_{exid}")
                    ]
                ]
                markup = InlineKeyboardMarkup(inline_keyboard=btn)
                await message.answer(ress, reply_markup=markup)
            else:
                await message.answer(ress, reply_markup=user_markup)
        else:
            await message.answer("No exam found with that code", reply_markup=user_markup)
    await state.clear()


@res.callback_query(results_states.choice)
async def choiceres(callback: CallbackQuery, state: FSMContext):
    if callback.data == "last":
        subm = db.fetchone("SELECT * FROM submissions WHERE userid = ? ORDER BY idx DESC", (callback.from_user.id,))
        if subm is not None:
            exam = db.fetchone("SELECT * FROM exams WHERE idx = ?", (subm[1],))
            if exam is not None:
                exid, title, about, total = exam[0], exam[2], exam[3], exam[4]
                # userid = db.fe
                ress = f"<b>Title: </b> {title}"
                ress += f"\n<b>Description: </b>{about}" if about != "__skip" else ""
                ress += f"\n<b>Number of questions: </b>{total}\n"
                ress += f"\n<b>Submitted: </b>{subm[3]} UTC"
                ress += f"\n<b>Correct answers:</b> {subm[4]} out of {total}\n<b>Percentage:</b> {round(100 * subm[4] / total, 2)}%"
                running = exam[6]
                if not running:
                    await state.update_data(corr=exam[5])
                    btn = [
                        [
                            InlineKeyboardButton(text="👁 Reveal the correct answers", callback_data=f"show_ans_{exid}")
                        ]
                    ]
                    markup = InlineKeyboardMarkup(inline_keyboard=btn)
                    await callback.message.answer(ress, reply_markup=markup)
                else:
                    await callback.message.answer(ress, reply_markup=user_markup)
            await state.clear()
        else:
            await callback.message.answer(f"You have never tried yet")

@res.callback_query()
async def show_anss(callback: CallbackQuery, state: FSMContext):
    if callback.data.split("show_ans_"):
        exid = callback.data.split("_")[2]
        data = await state.get_data()
        corr = list(db.fetchone("SELECT correct FROM exams WHERE idx = ?", (exid,))[0].split("__"))
        response = "✅ The correct solutions for the test were as follows:"
        for i in range(len(corr)):
            response += f"\n<b># {i + 1}</b>: {corr[i]}"
        await callback.message.answer(response)
