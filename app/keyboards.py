from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Задать вопрос 🥸", callback_data="question")],
    [InlineKeyboardButton(text="Помощь", callback_data="help")]
    ])

