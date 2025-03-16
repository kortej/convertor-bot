from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привіт, вибери дію!)", reply_markup=kb.main)


@router.message(F.text == 'Конвертація')
async def convert(message: Message):
    await message.answer(f'Виберіть формат:', reply_markup=kb.format_kb)