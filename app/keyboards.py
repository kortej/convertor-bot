from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/register'), KeyboardButton(text='/convert')]],
    resize_keyboard=True)


formats = ["PNG", "JPG", "WEBP"]

format_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=fmt)] for fmt in formats],
    resize_keyboard=True
)
