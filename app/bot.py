import asyncio
import logging
from datetime import datetime as dt
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from handlers.start_reg_stop import start_bot, stop_bot, start, secrete_key, verify
from database.sql import get_defaults
from handlers.prepare_and_print import prepare, andprint


logging.basicConfig(level=logging.INFO, 
                    filename=f'logs\\officeprinter_{dt.now().strftime("%Y-%m-%d_%H-%M")}.log',
                    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')

TOKEN = get_defaults('TOKEN')
ADMIN = get_defaults("ADMIN")
KEY = get_defaults('KEY')

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def printbot():
    dp.callback_query.register(verify, F.data.startswith('verify:'))
    dp.callback_query.register(andprint, F.data.startswith('print:'))
    dp.message.register(prepare, F.document)
    dp.message.register(start, CommandStart())
    dp.message.register(secrete_key, Command('code'))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(printbot())