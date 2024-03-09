import pystray as tr
import os
# import subprocess as sub
from winotify import Notification as N
from PIL import Image
from win32 import win32print as p
from database.sql import edit_defaults, get_defaults, db_start
from app.settings import settings

    
def tray():
    db_start()
    img = Image.open('assets\\alpha.png')

    def get_printers():
        printers = ['Default']
        for printer in p.EnumPrinters(p.PRINTER_ENUM_CONNECTIONS | p.PRINTER_ENUM_LOCAL):
            printers.append(printer[2])
        return printers

    def get_menu():
        global menu
        global selected
        menu = [tr.MenuItem('Настройки', select)]
        m_items = []
        selected = get_defaults('PRINTER')

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
        elif text=='Настройки':settings()
        elif text=='Обновить':None
        else:edit_defaults('PRINTER', text)
        get_menu()
        icon.update_menu()

    menu = get_menu()
    icon = tr.Icon('Office Printer', img, 'Office Printer', tr.Menu(*menu))
    icon.run()

    # process = sub.Popen('.venv/Scripts/python bot.py', creationflags=sub.CREATE_NO_WINDOW)
    # process.terminate()

    ico = os.path.join(os.getcwd(),'assets\logo.jpg')
    toast = N(app_id='Office Print',
                title='Бот остановлен!',
                msg='Бот успешно остановлен.\nДо новых встреч!',
                icon=ico)
    toast.show()