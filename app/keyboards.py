from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/convert')], [KeyboardButton(text='/my_stats'),
    KeyboardButton(text='/help'), KeyboardButton(text='/register')]],
    resize_keyboard=True)


formats = ["PNG", "JPG", "WEBP"]
formats_2 = ["TIFF", "ICO"]

format_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=fmt) for fmt in formats],
            [KeyboardButton(text=fmt_2) for fmt_2 in formats_2],
            [KeyboardButton(text='🔙 Назад')]],
    resize_keyboard=True
)
