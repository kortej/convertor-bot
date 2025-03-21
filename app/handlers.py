import os
import app.keyboards as kb
import database.requests as rq
import app.fsmContext as FSM
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from app.keyboards import formats, formats_2
from PIL import Image
from aiogram.types import FSInputFile
from dotenv import load_dotenv


router = Router()
load_dotenv()


ADMIN_ID = int(os.getenv('ADMIN_ID'))
user_format_choice = {}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSM.FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.reply("👑 Ласкаво просимо, Адміністоре!",
                            reply_markup=kb.admin_kb)
        await state.set_state(FSM.MenuStates.admin_main)
    else:
        await message.answer(f"✨ Привіт, виберіть дію: ",
                            reply_markup=kb.main)
        await state.set_state(FSM.MenuStates.sub_menu)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply('‼️Якщо є запитання або помітили якісь баги в боті, пишіть в підтримку: @nazardt ‼️')


@router.message(Command('register'))
async def cmd_registration(message: Message):
    if await rq.is_user_in_db(message.from_user.id) is False:
        await rq.set_user(message.from_user.id, message.from_user.first_name)
        await message.reply(text=f'✍🏻 Дякуємо за регістрацію!')
    else:
        await message.answer('📓 Ви вже зареєстровані)')


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
        response = "❌ Дані не знайдено.\nСпочатку зареєструйтеся!"

    await message.answer(response, parse_mode="Markdown")


@router.message(Command('all_users_stats'))
async def cmd_get_all_users(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer('🚫У вас немає прав на цю функцію🚫', reply_markup=kb.main)
    else:    
        users = await rq.get_all_users()

        response = "Список користувачів:\n\n"
        for user in users:
            response += (
                f"TG_ID: {user.tg_id}\n"
                f"Ім'я: {user.username}\n"
                f"Кількість конвертацій: {user.count_converts}\n\n"
                )
            
        await message.answer(response)


@router.message(F.text == '🔙 Назад')
async def back_to_main(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer('🤴 Головне меню Адміна', reply_markup=kb.admin_kb)
    else:
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
