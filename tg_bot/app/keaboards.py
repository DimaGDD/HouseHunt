from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


start_keaboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='▶️ Open WebApp', web_app=WebAppInfo(url='https://dimagdd.github.io/HouseHunt/'))]
    ]
)