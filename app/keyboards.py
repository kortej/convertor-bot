from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Конвертація')]
])


formats = ["PNG", "JPG", "WEBP"]

format_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=fmt)] for fmt in formats],
    resize_keyboard=True
)
