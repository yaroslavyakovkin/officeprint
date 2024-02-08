from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Стартовое сообщение.'
        ),
        BotCommand(
            command='settings',
            description='Настройки печати по умолчанию'
        ),
        BotCommand(
            command='code',
            description='Верификация с помощью кода'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())