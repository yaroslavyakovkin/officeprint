import os, asyncio, logging, shutil
from subprocess import call as printprocess
from docx2pdf import convert as d2p
from win32 import win32api, win32print
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from database.sql import get_verify, create_file, delete_file, get_settings, edit_settings
from util.keyboards import kbmain, kbsett
from util.checking import STATUS, ALLOWED_EXTENSIONS


async def prepare(message:Message, bot:Bot):
    verify = await get_verify(message.from_user.id)
    if verify is None or verify[0] == 0:
        await message.answer('<i>Вы еще не прошли верификацию!</i>', parse_mode=ParseMode.HTML)
    else:
        if message.document.file_size <= 20971520:
            name, ext = os.path.splitext(message.document.file_name)
            if ext in ALLOWED_EXTENSIONS:    
                logging.info(f'User({message.from_user.id}) UPLOAD new allowed file!')
                settings = await create_file(message.document.file_unique_id)

                copy = settings[0]
                if settings[1] == 1: color='ч/б' 
                else:color = 'цвет'
                if settings[2] == 1: duplex = 'Односторонняя печать'
                elif settings[2] == 2: duplex = 'Двусторонняя печать\nПереплет сбоку'
                elif settings[2] == 3: duplex = 'Двусторонняя печать\nПереплет сверху'

                await message.answer_document(message.document.file_id, 
                                            caption=f'<i>Файл <code>{name}</code> принят!\n\
                                                       \nЧисло экземпляров: {copy}\
                                                       \nЦвет печати: {color}\
                                                       \n{duplex}</i>',parse_mode=ParseMode.HTML,
                                            reply_markup=kbmain)
            else:
                await message.reply(f'<b>Ой, файл не того формата!</b>', parse_mode=ParseMode.HTML)
        else:
            await message.reply(f'<b>Ой, файл слишком большой!</b>', parse_mode=ParseMode.HTML)

async def andprint(call:CallbackQuery, bot:Bot):
    data = call.data.split(':')
    file_id = call.message.document.file_unique_id
    name, ext = os.path.splitext(call.message.document.file_name)
    settings = await get_settings(file_id)
    copy = settings[0]
    color = settings[1]
    duplex = settings[2]

    if data[1] == 'back':
        await call.message.edit_reply_markup(reply_markup=kbmain)

    if data[1] == 'copy':
        if data[2] == 'add': copy += 1
        elif copy == 1: await call.answer('Меньше только не печатать...')
        else: copy -= 1
        await edit_settings(file_id, 'copy', copy)
  
    if data[1] == 'color':
        if data[2] == 'clr':
            if color != 2: color = 2
            else: await call.answer('Цвет уже цветной!')
        else:
            if color != 1: color = 1
            else: await call.answer('Цвет уже черно-белый!')
        await edit_settings(file_id, 'color', color)

    if data[1] == 'duplex':
        if data[2] == 'twoup':
            if duplex != 3: duplex = 3
            else: await call.answer('Печать уже двусторонняя и с переплётом сверху!')
        elif data[2] == 'twonear':
            if duplex != 2: duplex = 2
            else: await call.answer('Печать уже двусторонняя и с переплётом сбоку!')
        elif data[2] == 'oneside':
            if duplex != 1: duplex = 1
            else: await call.answer('Печать уже односторонняя!')
        await edit_settings(file_id, 'duplex', duplex)
    
    if data[1] == 'print':
        if color == 1: clr='ч/б' 
        else:color = 'цвет'
        if duplex == 1: dpl = 'Односторонняя печать'
        elif duplex == 2: dpl = 'Двусторонняя печать\nПереплет сбоку'
        elif duplex == 3: dpl = 'Двусторонняя печать\nПереплет сверху'

        caption=f'<i>Файл <code>{name}</code> принят!\n\
                \nЧисло экземпляров: {copy}\
                \nЦвет печати: {clr}\
                \n{dpl}</i>\n\
                \n<b>Статус:\
                \nПодготовка файла'
        await call.message.edit_caption(caption=f'{caption}</b>',parse_mode=ParseMode.HTML)
        
        printer_name = win32print.GetDefaultPrinter()
        default = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
        handle = win32print.OpenPrinter(printer_name, default)
        path = f'temp\\{file_id}'
        pdf = f'{path}\\{name}.pdf'
        tempath = f'{path}\\{name}{ext}'
        
        caption += '\nСкачивание файла'
        await call.message.edit_caption(caption=f'{caption}</b>',parse_mode=ParseMode.HTML)

        if not os.path.exists(path):os.makedirs(path)
        file_info = await bot.get_file(call.message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        with open(tempath, "wb") as new_file:
            new_file.write(downloaded_file.read())

        if ext != '.pdf':
            caption += '\nКонвертация файла'
            await call.message.edit_caption(caption=f'{caption}</b>',parse_mode=ParseMode.HTML)
            d2p(tempath)
            os.remove(tempath)

        for i in range(3600):
            t = "{:02d}:{:02d}".format(i // 60, i % 60)
            if win32print.EnumJobs(handle, 0, 1):
                wait = caption + '\nОжидает печать - '
                await call.message.edit_caption(caption=f'{wait}{t}</b>',parse_mode=ParseMode.HTML)
            else: 
                if i == 0: caption += f'\nПринят в печать'
                else: caption = f'{wait}{t}\nПринят в печать'
                break
            await asyncio.sleep(1)
        else:await call.message.edit_caption(caption=f'Что-то пошло не так...')

        
        attributes = win32print.GetPrinter(handle, 2)
        attributes['pDevMode'].Copies = copy
        attributes['pDevMode'].Color = color
        attributes['pDevMode'].Duplex = duplex
        win32print.SetPrinter(handle, 2, attributes, 0)  
        printprocess(['util\\sumatra\\SumatraPDF.exe', '-print-to-default', '-silent', pdf])
        #win32api.ShellExecute(2,'print',pdf, None, '.', 0)
        await asyncio.sleep(5)

        caption += '\nПечатается - '
        r = 0
        for i in range(3600):
            t = "{:02d}:{:02d}".format(i // 60, i % 60)
            await call.message.edit_caption(caption=f'{caption}{t}</b>',parse_mode=ParseMode.HTML)
            status = win32print.GetPrinter(handle, 2)['Status']
            job = win32print.EnumJobs(handle, 0, 1)
            if not job: break
            if status !=0 and report:
                logging.error(f'ERROR #{status} on PRINTER!')
                report = False
                r = i
                if status in STATUS:
                    await bot.send_message(os.getenv('ADMIN'),f'Во время печати произошла ошибка\
                                                        №{status}\nТекст ошибки: {STATUS[status]}')
            if i == 0 or i-r == 60:report = True
            await asyncio.sleep(1)
        else:await call.message.edit_caption(caption=f'Что-то пошло не так...')

        caption += f'{t}\nФайл успешно напечатан!'
        logging.info(f'file for USER({call.from_user.id}) successful PRINTED!')
        await call.message.edit_caption(caption=
                                        f'{caption}</b>',
                                        parse_mode=ParseMode.HTML)
        await delete_file(file_id)
        shutil.rmtree(path)

    if data[1] == 'cancel':
        await delete_file(file_id)
        await call.answer('Заявка успешно отменена.')
        await call.message.delete()

    if data[1] != 'print' and data[1] != 'cancel' and data[1] != 'back':
        if color == 1: clr='ч/б' 
        else:clr = 'цвет'
        if duplex == 1: dpl = 'Односторонняя печать'
        elif duplex == 2: dpl = 'Двусторонняя печать\nПереплет сбоку'
        elif duplex == 3: dpl = 'Двусторонняя печать\nПереплет сверху'

        await call.message.edit_caption(caption=f'<i>Файл <code>{name}</code> принят!\n\
                                                \nЧисло экземпляров: {copy}\
                                                \nЦвет печати: {clr}\
                                                \n{dpl}</i>', parse_mode=ParseMode.HTML,
                                                reply_markup=kbsett)