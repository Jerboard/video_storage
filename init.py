from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode

from datetime import datetime

import traceback
import logging

from dotenv import load_dotenv
from os import getenv
from pytz import timezone

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

import asyncio
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

load_dotenv ()
loop = asyncio.get_event_loop()
dp = Dispatcher()
bot = Bot(getenv("TOKEN"), parse_mode=ParseMode.HTML)


TZ = timezone('Europe/Moscow')

DATETIME_STR_FORMAT = '%d.%m.%y %H:%M'

ENGINE = create_async_engine(url=getenv('DB_URL'))


async def set_main_menu() -> None:
    main_menu_commands = [
        BotCommand (command='/start',
                    description='Перезапуск'),
    ]

    await bot.set_my_commands(main_menu_commands)


def log_error(message):
    timestamp = datetime.now(TZ)
    filename = traceback.format_exc()[1]
    line_number = traceback.format_exc()[2]
    logging.error(f'{timestamp} {filename} {line_number}: {message}')