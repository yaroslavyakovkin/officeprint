from threading import Thread
from asyncio import run
from app.bot import printbot
from app.tray import tray


def main():
    trayproc = Thread(target=tray)
    botproc = Thread(target=run, args=(printbot(),), daemon=True)
    trayproc.start()
    botproc.start()
    trayproc.join()

if __name__ == '__main__':
    main()