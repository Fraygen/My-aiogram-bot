from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from app.openrouter import get_answer, OpenRouterChatSession

import app.keyboards as kb
import asyncio
import logging


logger = logging.getLogger(__name__)
router = Router()
user_chats = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}.\n"
                         f"Я твой ИИ-Помощник, можешь задавать мне любые вопросы!",
                         reply_markup=kb.start)    


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        f"🤖 **Помощь по боту**\n\n"
        f"Просто напишите мне любое сообщение, а я отвечу\n"
        f" /start - перезапустить бота\n"
        f" /help - информация о боте\n"
        f" /clear - очистить историю диалога\n"
        f" /ask - задать вопрос"
    )


@router.message(Command("ask"))
async def cmd_ask(message: Message):
    await message.answer("Задавай свой вопрос! Я постараюсь помочь 😊")


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    user_id = message.from_user.id
    if user_id in user_chats:
        del user_chats[user_id]
        await message.answer("🧹 История очищена!")
    else:
        await message.answer("🤷 Истории и так нет")



@router.callback_query(F.data == "question")
async def question_button(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_ask(callback.message)


@router.callback_query(F.data == "help")
async def help_button(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_help(callback.message)


async def typing_animation(message: Message, text: str = 'Thinking'):
    msg = await message.answer(f"{text}.")
    await asyncio.sleep(0.5)
    await msg.edit_text(f"{text}..")
    await asyncio.sleep(0.5)
    await msg.edit_text(f"{text}...")
    await asyncio.sleep(0.5)
    await msg.delete()


@router.message(F.text)
async def simple_question(message: Message):
    user_id = message.from_user.id
    user_text = message.text
    
    logger.info(f"От {message.from_user.first_name}: {user_text[:100]}...")
    
    await typing_animation(message)
    
    try:
        if user_id not in user_chats:
            user_chats[user_id] = OpenRouterChatSession()
        
        chat = user_chats[user_id]
        answer = chat.send_message(user_text)
        
        if len(answer) > 4000:
            answer = answer[:3500] + "...\n\n✂️ (ответ сокращен)"
        
        await message.answer(answer)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer(f"😔 Ошибка: {str(e)[:150]}")






































''' # Этот хендлер будет логировать ВСЕ сообщения (должен быть САМЫМ ПЕРВЫМ!)
@router.message()
async def log_all_messages(message: Message):
    # Формируем информацию о пользователе
    user_id = message.from_user.id
    username = message.from_user.username or "нет username"
    first_name = message.from_user.first_name
    
    # Определяем тип сообщения
    if message.text:
        msg_type = "📝 Текст"
        content = message.text
    elif message.photo:
        msg_type = "🖼 Фото"
        content = f"ID фото: {message.photo[-1].file_id}"
    elif message.sticker:
        msg_type = "🎭 Стикер"
        content = f"ID стикера: {message.sticker.file_id}"
    else:
        msg_type = "📦 Другое"
        content = "не текст"
    
    # Красивое логирование
    print(f"\n{'='*50}")
    print(f"🕐 {message.date.strftime('%H:%M:%S')}")
    print(f"👤 {first_name} (@{username}) [ID: {user_id}]")
    print(f"📌 Тип: {msg_type}")
    print(f"💬 {content}")
    
    # Если это команда
    if message.text and message.text.startswith('/'):
        print(f"⚡ КОМАНДА: {message.text}")
    
    print(f"{'='*50}\n")
    
    # ВАЖНО: продолжаем обработку сообщения
    # Не делаем return, чтобы сообщение пошло дальше к другим хендлерам '''