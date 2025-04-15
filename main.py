import asyncio
import os
from aiogram import Bot, Dispatcher

from app.handlers import router
from dotenv import load_dotenv

load_dotenv()




async def main():
    bot_token = os.getenv('TOKEN')
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('Бот включен')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
