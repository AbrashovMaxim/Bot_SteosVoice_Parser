from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.dispatcher import Dispatcher
import asyncio

from libs.other import router
from libs.config import config

async def main():
    bot = Bot(token=config.get_token_tg(), parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
