import os
import shutil
from app.settings import settings
from util.sql import db_start, get_defaults
from winotify import Notification as N


db_start()
if get_defaults('TOKEN') is None:
    settings()
    if get_defaults('TOKEN') is None:
        ico = os.path.join(os.getcwd(),'assets\logo.jpg')
        toast = N(app_id='Office Print',
            title='Требуется токен!',
            msg='Вы не указали токен. Перезапустите приложение, затем попробуйте еще раз.',
            icon=ico)
        toast.show()
        exit()
from threading import Thread
from asyncio import run
from app.bot import printbot
from app.tray import tray
trayproc = Thread(target=tray)
trayproc.start()
botproc = Thread(target=run, args=(printbot(),), daemon=True)
botproc.start()
trayproc.join()
if os.path.exists('temp'):shutil.rmtree('temp')