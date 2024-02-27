import asyncio
import logging
import os
import threading as th
import pystray as tr
from PIL import Image
from win32 import win32print as p
from datetime import datetime as dt
from dotenv import load_dotenv as ld
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from handlers.start_reg_stop import start_bot, stop_bot, start, secrete_key, verify
from database.sql import db_start, edit_defaults, get_defaults
from handlers.prepare_and_print import prepare, andprint


ld()
TOKEN = os.getenv('TOKEN_TEST')
ADMIN = os.getenv("ADMIN")
KEY = os.getenv('KEY')

logging.basicConfig(level=logging.INFO, 
                    filename=f'logs\\officeprinter_{dt.now().strftime("%Y-%m-%d_%H-%M")}.log',
                    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')

bot = Bot(token=TOKEN)
dp = Dispatcher()
db_start()

def tray():
    img = Image.open('assets\\alpha.png')
    def get_printers():
        printers = ['Default']
        for printer in p.EnumPrinters(p.PRINTER_ENUM_CONNECTIONS | p.PRINTER_ENUM_LOCAL):
            printers.append(printer[2])
        return printers

    def get_menu():
        global menu
        global selected
        menu = []
        m_items = []
        selected = get_defaults('printer')

        for printer in get_printers():
            m_items += [tr.MenuItem(printer, select, lambda _, item = printer: item == selected)]

        m_items += [tr.MenuItem('Обновить', select)]
        menu += [tr.MenuItem('Принтеры', tr.Menu(*m_items))]
        menu += [tr.MenuItem('Выход', select)]
        return menu

    def select(icon, item):
        text = item.text
        if text=='Выход':
            icon.stop()
        elif text=='Обновить':None
        else:edit_defaults('printer', text)
        get_menu()
        icon.update_menu()

    menu = get_menu()
    icon = tr.Icon('Office Printer', img, 'Office Printer', tr.Menu(*menu))

    icon.run()

async def printbot():
    global trayproc
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
    trayproc = th.Thread(target=tray)
    trayproc.start()
    asyncio.run(printbot())