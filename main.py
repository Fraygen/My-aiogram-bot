import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import TOKEN
from app.handlers import router
from colorama import Fore, Style

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")

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

    try:
        logging.info(f"{Fore.GREEN}✅ БОТ ЗАПУЩЕН ✅{Style.RESET_ALL}")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(f"{Fore.GREEN}✅ БОТ УСПЕШНО ОСТАНОВЛЕН ✅{Style.RESET_ALL}")