from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import app.keyboards as kb
from app.keyboards import formats


router = Router()

user_format_choise = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привіт, вибери формат для конвертації!: ", reply_markup=kb.format_kb)


@router.message(F.text.in_(formats))
async def choose_format(message: Message):
    user_format_choise[message.from_user.id] = message.text.lower()
    await message.answer(f"✅ Формат {hbold(message.text)} вибрано. Тепер надішли фото!",
                        parse_mode="HTML")