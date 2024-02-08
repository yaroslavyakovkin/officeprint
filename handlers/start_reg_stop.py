import os, logging
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.sql import db_start, get_verify, create_user, switch_verify, get_username
from util.commands import commands


async def start_bot(bot:Bot):
    await commands(bot)
    await db_start()
    print('BOT STARTED')

async def start(message:Message, bot:Bot):
    user_id = message.from_user.id
    username = message.from_user.username
    verify = await get_verify(message.from_user.id)
    if verify is None:
        await create_user(user_id, username)
        kb = InlineKeyboardBuilder()
        kb.button(text='Разрешить доступ', callback_data=f'verify:{user_id}')
        await message.answer('🖨')
        await message.answer('<i>Вы у нас впервые?\
                             \n<b>Дождитесь верификации от администратора!</b>\
                             \nИли вы можете прислать секретный код через команду</i> <code>/code</code>',
                             parse_mode=ParseMode.HTML)
        await bot.send_message(os.getenv('ADMIN'), f'Новый пользователь @{message.from_user.username}',reply_markup=kb.as_markup())
    elif verify[0] == 1: await message.answer('Добро пожаловать снова!\nЧто отправим на печать?')

async def secrete_key(message:Message, bot:Bot):
    if message.text.split(' ')[1] == os.getenv('KEY'):
        user_id = message.from_user.id
        username = message.from_user.username
        verify = await get_verify(user_id)
        if verify is None: await create_user(user_id, username); verify = (0,)
        if verify[0] == 1: await message.reply('У вас уже есть доступ...')
        else:
            await switch_verify(user_id)
            await message.answer('Доступ разрешён!\nТеперь можно присылать файлы!')
            logging.info(f'USER({user_id}) verifed with SECRET-KEY!')
            await bot.send_message(os.getenv('ADMIN'), f'Пользователь @{username}, получил доступ через ключ.')
    else: await message.reply('Введён неверный код...')


async def verify(call:CallbackQuery, bot:Bot):
    user_id=call.data.split(':')[1]
    if await get_verify(user_id)[0] == 1:
        call.message.delete()
    else:
        await switch_verify(user_id)
        await call.message.edit_text(f'Доступ для пользователя @{await get_username(user_id)} разрешён!')
        logging.info(f'USER({user_id}) verifed by ADMIN!')
        await bot.send_message(user_id, 'Доступ разрешён! Теперь можно присылать файлы!')

async def stop_bot():
    print('BOT STOPPED')