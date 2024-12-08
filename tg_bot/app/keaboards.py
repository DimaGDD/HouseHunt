from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

start_keaboard = InlineKeyboardMarkup(
	inline_keyboard=[InlineKeyboardButton(text='Узнать цену', callback_data='get_price')]
)