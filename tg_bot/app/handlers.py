from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandObject, CommandStart

from app.text import start_message

router = Router()

user_data = {}

@router.message(CommandStart())
async def start(message: Message):
    """Приветственное сообщение с кнопкой для меню"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Узнать цену", callback_data="get_price")]
        ]
    )
    await message.answer(start_message, reply_markup=keyboard)

@router.callback_query(F.data == "get_price")
async def show_price_menu(callback: CallbackQuery):
    """Показывает меню для ввода параметров"""
    
    keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Количество комнат")],
        [KeyboardButton(text="Площадь")],
        [KeyboardButton(text="Этаж")],
        [KeyboardButton(text="Район")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

    user_data[callback.from_user.id] = {"step": "rooms"}

    await callback.message.answer("Введите количество комнат:", reply_markup=keyboard)
    await callback.answer()

@router.message()
async def process_input(message: Message):
    """Обработка ввода пользователя"""
    chat_id = message.from_user.id
    if chat_id not in user_data:
        await message.answer("Пожалуйста, начните с команды /start.")
        return

    step = user_data[chat_id].get("step")

    if step == "rooms":
        try:
            rooms = int(message.text)
            user_data[chat_id]["rooms"] = rooms
            user_data[chat_id]["step"] = "area"
            await message.answer("Введите площадь квартиры (м²):")
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число для комнат.")

    elif step == "area":
        try:
            area = float(message.text)
            user_data[chat_id]["area"] = area
            user_data[chat_id]["step"] = "floor"
            await message.answer("Введите этаж:")
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число для площади.")

    elif step == "floor":
        try:
            floor = int(message.text)
            user_data[chat_id]["floor"] = floor
            user_data[chat_id]["step"] = "district"
            await message.answer("Введите район:")
        except ValueError:
            await message.answer("Пожалуйста, введите корректное число для этажа.")

    elif step == "district":
        district = message.text.strip()
        user_data[chat_id]["district"] = district

        # Пример: вычисление цены
        rooms = user_data[chat_id]["rooms"]
        area = user_data[chat_id]["area"]
        floor = user_data[chat_id]["floor"]
        price = rooms * area * floor * 1000  # Заглушка логики расчета

        await message.answer(
            f"Квартира с параметрами:\n"
            f"- Количество комнат: {rooms}\n"
            f"- Площадь: {area} м²\n"
            f"- Этаж: {floor}\n"
            f"- Район: {district}\n"
            f"Цена: {price} руб."
        )

        user_data.pop(chat_id, None)  # Очистка данных

    else:
        await message.answer("Пожалуйста, начните с команды /start.")
