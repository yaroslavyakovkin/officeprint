import asyncio
import logging
import os
from datetime import datetime as dt
from dotenv import load_dotenv as ld
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from handlers.start_reg_stop import start_bot, stop_bot, start, secrete_key, verify
from handlers.prepare_and_print import prepare, andprint


ld()
TOKEN = os.getenv('TOKEN')
ADMIN = os.getenv("ADMIN")
KEY = os.getenv('KEY')

logging.basicConfig(level=logging.INFO, 
                filename=f'logs\\officeprinter_{dt.datetime.now().strftime("%Y-%m-%d_%H-%M")}.log',
            format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
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

def stop(signum, frame):
    exit()    

if __name__ == '__main__':    
    asyncio.run(main())