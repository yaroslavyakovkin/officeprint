import os
import sqlite3
import logging
from datetime import datetime


def db_start():
    if not os.path.exists('database'):os.makedirs('database')
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()

    cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS users
                (
                user_id INTEGER, 
                username TEXT,
                verify INTEGER DEFAULT 0,
                PRIMARY KEY("user_id")
                )
                '''
                )
    
    cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS files
                (
                unique_id TEXT,
                copy INTEGER DEFAULT 1,
                color INTEGER DEFAULT 1,
                duplex INTEGER DEFAULT 1,
                date TEXT,
                username TEXT
                )
                '''
                )

    cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS defaults
                (
                key TEXT,
                value TEXT,
                PRIMARY KEY('key')
                )
                '''
                )
    try:
        cur.execute("INSERT INTO defaults (key, value) VALUES (?, ?)", ('PRINTER', 'Default'))
        cur.execute("INSERT INTO defaults (key) VALUES (?)", ('TOKEN',))
        cur.execute("INSERT INTO defaults (key) VALUES (?)", ('ADMIN',))
        cur.execute("INSERT INTO defaults (key) VALUES (?)", ('KEY',))
    except sqlite3.IntegrityError:None
    finally:
        db.commit()
        db.close()

async def create_user(user_id:int, username:str):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    user = cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if user:
        if user[0] != username:
            cur.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            db.commit()
    else:
        logging.info(f'New user registered! user_id:{user_id}')
        cur.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        db.commit()
    db.close()

async def get_verify(user_id:int):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    verify = cur.execute('SELECT verify FROM users WHERE user_id=?',(user_id,)).fetchone()
    db.close()
    return verify

async def get_username(user_id:int):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    username = cur.execute('SELECT username FROM users WHERE user_id=?',(user_id,)).fetchone()
    db.close()
    return username[0]

async def switch_verify(user_id:int):
    verify = await get_verify(user_id)
    if verify[0] == 0: v = 1 
    else: v = 0
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    cur.execute('UPDATE users SET verify = ? WHERE user_id = ?', (v, user_id))
    db.commit()
    db.close()

async def create_file(unique_id:str, username:str):
    date = datetime.now().strftime('%d.%m.%Y - %H:%M')
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    cur.execute("INSERT INTO files (unique_id, date, username) VALUES (?, ?, ?)", (unique_id, date, username))
    db.commit()
    db.close()
    return await get_settings(unique_id)

async def delete_file(unique_id:str):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM files WHERE unique_id = ?", (unique_id,))
        db.commit()
    finally:
        db.close()

async def get_settings(unique_id:str):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    cur.execute('SELECT copy, color, duplex FROM files WHERE unique_id=?',(unique_id,))
    settings = cur.fetchone()
    db.close()
    return settings

async def edit_settings(unique_id:str, parametr:str, value:int):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    cur.execute(f'UPDATE files SET {parametr} = ? WHERE unique_id = ?', (value, unique_id))
    db.commit()
    db.close()

def edit_defaults(key:str, value:str):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    cur.execute(f'UPDATE defaults SET value = ? WHERE key = ?', (value, key))
    db.commit()
    db.close()

def get_defaults(key:str):
    db = sqlite3.connect('database\\db.sql')
    cur = db.cursor()
    value = cur.execute('SELECT value FROM defaults WHERE key = ?',(key,)).fetchone()
    db.close()
    return value[0]