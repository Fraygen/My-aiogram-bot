import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import TOKEN
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():

    commands = [
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="❓ Помощь"),
        BotCommand(command="ask", description="🤔 Задать вопрос"),
        BotCommand(command="clear", description="🧹 Очистить историю")
    ]

    await bot.set_my_commands(commands)

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)

    try:
        print("✅ БОТ ЗАПУЩЕН ✅")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("✅ БОТ УСПЕШНО ОСТАНОВЛЕН ✅")