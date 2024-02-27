import asyncio
from bot import printbot
from tray import tray

def main():
    shutdown = asyncio.Event()
    loop = asyncio.get_event_loop()
    bot = loop.create_task(printbot())
    loop.run_until_complete(tray())
    bot.cancel()
    try:
        loop.run_until_complete(bot)
    except asyncio.CancelledError:
        pass

if __name__ == '__main__':
    main()