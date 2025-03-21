import os
import app.keyboards as kb
import database.requests as rq
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from app.keyboards import formats, formats_2
from PIL import Image
from aiogram.types import FSInputFile
import app.fsmContext as FSM


router = Router()

user_format_choice = {}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSM.FSMContext):
    await message.answer(f"Привіт, виберіть дію: ",
                        reply_markup=kb.main)
    await state.set_state(FSM.MenuStates.sub_menu)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply('Якщо є запитання або помітили якісь баги в боті, пишіть в підтримку: @nazardt')


@router.message(Command('register'))
async def cmd_registration(message: Message):
    if await rq.is_user_in_db(message.from_user.id) is False:
        await rq.set_user(message.from_user.id, message.from_user.first_name)
        await message.reply(text=f'Дякуємо за регістрацію!')
    else:
        await message.answer('Ви вже зареєстровані)')


@router.message(Command('convert'))
async def cmd_convertion(message: Message):
    await message.answer(text='Виберіть формат: ', reply_markup=kb.format_kb)


@router.message(Command('my_stats'))
async def send_user_data(message: Message):
    user_id = message.from_user.id
    user = await rq.get_user(user_id)

    if user:
        response = f"👤 *Користувач:* {user.username}\n🎯 *Конвертації:* {user.count_converts}"
    else:
        response = "❌ Дані не знайдено."

    await message.answer(response, parse_mode="Markdown")


@router.message(F.text == '🔙 Назад')
async def back_to_main(message: Message): # remove state: FSM.FSMContext
    await message.answer('🔹 Головне меню', reply_markup=kb.main)


@router.message(F.text.in_(formats) | F.text.in_(formats_2))
async def choose_format(message: Message):
    user_format_choice[message.from_user.id] = message.text.lower()
    await message.answer(f"✅ Формат {hbold(message.text)} вибрано. Тепер надішли фото!",
                        parse_mode="HTML")
    

@router.message(F.photo)
async def handle_photo(message: Message):
    user_id = message.from_user.id

    # Перевіряємо, чи користувач вибрав формат
    if user_id not in user_format_choice:
        await message.answer("❌ Спочатку вибери формат!", reply_markup=kb.format_kb)
        return

    format_to_convert = user_format_choice[user_id]

    # Перевіряємо формат і замінюємо "JPG" на "JPEG"
    if format_to_convert.lower() == "jpg":
        format_to_convert = "JPEG"
    else:
        format_to_convert = format_to_convert.upper()

    bot = message.bot

    # Завантажуємо фото
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    input_path = f"temp_input{user_id}.jpg"
    output_path = f"converted_{user_id}.{format_to_convert}"

    await bot.download_file(file_path, input_path)

    # Конвертація фото
    img = Image.open(input_path)
    img.convert("RGB").save(output_path, format_to_convert.upper())

    # Відправка назад
    converted_photo = FSInputFile(output_path)
    await message.answer_document(converted_photo)

    await rq.counter(tg_id=user_id)

    # Очищення файлів
    os.remove(input_path)
    os.remove(output_path)
