import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from database.db import async_main
import os
from dotenv import load_dotenv

load_dotenv()


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN')) 
    dp = Dispatcher() 
    dp.include_router(router) # передаем роутер в диспетчер
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) 


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
