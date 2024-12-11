import webbrowser
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart

from app.text import start_message
from app.keaboards import start_keaboard


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    keyboard = start_keaboard
    await message.answer(start_message, reply_markup=keyboard)