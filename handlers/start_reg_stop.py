import os
import logging
from winotify import Notification as N
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from util.sql import get_verify, create_user, switch_verify, get_username, get_defaults
from util.commands import commands

async def start_bot(bot:Bot):
    print('Hiiiii! My cmd-friend...')
    info = await bot.get_me()
    url = f'https://t.me/{info.username}'
    ico = os.path.join(os.getcwd(),'assets\logo.jpg')
    toast = N(app_id='Office Print', 
              title='Бот запущен!',
              msg='Бот успешно запущен, воспользуйтесь иконкой в трее для выбора принтера.',
              icon=ico)
    toast.add_actions(label='Telegram',
                      launch=url)
    toast.show()
    # await commands(bot)

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
                             \nИли пришлите секретный код через команду</i> \<code>/code</code>',
                             parse_mode=ParseMode.HTML)
        await bot.send_message(get_defaults("ADMIN"), 
                               f'Новый пользователь @{message.from_user.username}',
                               reply_markup=kb.as_markup())
    elif verify[0] == 1: await message.answer('Добро пожаловать снова!\nЧто отправим на печать?')

async def secrete_key(message:Message, bot:Bot):
    if message.text.split(' ')[1] == get_defaults("KEY"):
        user_id = message.from_user.id
        username = message.from_user.username
        verify = await get_verify(user_id)
        if verify is None: await create_user(user_id, username); verify = (0,)
        if verify[0] == 1: await message.reply('У вас уже есть доступ...')
        else:
            await switch_verify(user_id)
            await message.answer('Доступ разрешён!\nТеперь можно присылать файлы!')
            logging.info(f'USER({user_id}) verifed with SECRET-KEY!')
            await bot.send_message(get_defaults("ADMIN"),
                                   f'Пользователь @{username}, получил доступ через код.')
    else: await message.reply('Введён неверный код...')


async def verify(call:CallbackQuery, bot:Bot):
    user_id=int(call.data.split(':')[1])
    verify = await get_verify(user_id)
    if verify[0] == 1:
        call.message.delete()
    else:
        await switch_verify(user_id)
        await call.message.edit_text(f'Доступ для пользователя @{await get_username(user_id)} разрешён!')
        logging.info(f'USER({user_id}) verifed by ADMIN!')
        await bot.send_message(user_id, 'Доступ разрешён! Теперь можно присылать файлы!')

# Эта штука к сожалению не работает, надо будет разобраться, как мягко выключить бота.
async def stop_bot():
    print('Bye! My cmd-friend...')
    ico = os.path.join(os.getcwd(),'assets\logo.jpg')
    toast = N(app_id='Office Print',
            title='Бот остановлен!',
            msg='Бот успешно остановлен.\nДо новых встреч!',
            icon=ico)
    toast.show()