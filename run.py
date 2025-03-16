import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router


bot = Bot(token=TOKEN) 
dp = Dispatcher() 


async def main():
    dp.include_router(router) # передаем роутер в диспетчер
    await dp.start_polling(bot) 


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
