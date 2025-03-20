from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/convert')], [KeyboardButton(text='/my_stats'),
    KeyboardButton(text='/help'), KeyboardButton(text='/register')]],
    resize_keyboard=True)


formats = ["PNG", "JPG", "WEBP", "TIFF", "ICO"]

format_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=fmt) for fmt in formats]],
    resize_keyboard=True
)
