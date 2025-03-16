from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"ТЕСТ НОМЕР 1")