import asyncio
import aiogram
import logging
import os

from aiogram import Bot, Dispatcher
from app.handlers import router

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    logging.info("Starting bot...")
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')