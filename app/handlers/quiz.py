from aiogram import F, types, Router
from aiogram.filters.command import Command
from aiogram.types.message import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.db.quiz_controller import get_quiz_index, update_quiz_index
from app.db.quiz_db import quiz_data
from app.keyboard import generate_options_keyboard

quiz_router = Router()


@quiz_router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, correct=True)


@quiz_router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, correct=False)


async def handle_answer(callback: types.CallbackQuery, correct: bool):
    # fix pyright errors
    if (
        callback.bot is None
        or not isinstance(callback.message, Message)
        or callback.message.from_user is None
    ):
        raise ValueError("Input data from teleram contains None")

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )

    current_question_index, correct_answers = await get_quiz_index(
        callback.from_user.id
    )

    if correct:
        correct_answers += 1
        await callback.message.answer("Верно!")
    else:
        correct_option = quiz_data[current_question_index]["correct_option"]
        await callback.message.answer(
            f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"
        )

    current_question_index += 1
    await update_quiz_index(
        callback.from_user.id, current_question_index, correct_answers
    )

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer(
            f"Это был последний вопрос. Квиз завершен!\n Вы ответили верно на {correct_answers}/{len(quiz_data)}"
        )


@quiz_router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer(
        "Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True)
    )


@quiz_router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    # fix pyright
    if message.from_user is None:
        raise ValueError("Input data from teleram contains None")

    _, correct_answers = await get_quiz_index(
        message.from_user.id
    )
    await message.answer(f"Ваш последний квест: {correct_answers}/{len(quiz_data)}")


@quiz_router.message(F.text == "Начать игру")
@quiz_router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)


async def new_quiz(message: types.Message):
    # fix pyright errors
    if message.from_user is None:
        raise ValueError("Input data from teleram contains None")

    user_id = message.from_user.id
    current_question_index = 0
    correct_answer = 0
    await update_quiz_index(user_id, current_question_index, correct_answer)
    await get_question(message, user_id)


async def get_question(message: types.Message, user_id: int):
    current_question_index, _ = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]["correct_option"]
    opts = quiz_data[current_question_index]["options"]
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(
        f"{quiz_data[current_question_index]['question']}", reply_markup=kb
    )
