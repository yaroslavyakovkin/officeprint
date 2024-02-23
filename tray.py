import pystray as tr
import signal as s
import time as t
import os
import subprocess as sub
from PIL import Image
from win32 import win32print as p
from database.sql import db_start, edit_defaults, get_defaults

    
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

process = sub.Popen('.venv/Scripts/python bot.py')
menu = get_menu()
icon = tr.Icon('Office Printer', img, 'Office Printer', tr.Menu(*menu))
t.sleep(1)
icon.run()
os.kill(process.pid, s.CTRL_C_EVENT)