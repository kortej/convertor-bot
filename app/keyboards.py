from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyb = ReplyKeyboardMarkup(keyboard=
    [[KeyboardButton(text='Profile'), KeyboardButton(text='Convert')]],
    resize_keyboard=True
)


formats = ["PNG", "JPG", "WEBP"]

format_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=fmt)] for fmt in formats],
    resize_keyboard=True
)
