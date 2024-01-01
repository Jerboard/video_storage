from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


import json
from datetime import datetime

import db
from init import dp, TZ, bot
from utils.message_utils import proces_entities
from keayboards import inline_kb as kb


# команда старт
@dp.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    text = ('Привет друг!\n'
            'Это простой не коммерческий проект где ты сможешь сохранить любимые фильмы или '
            'посмотреть видео других пользователей\n\n'
            'Всё прост: кидай фильмы из ТГ, и ты, и другие пользователи, смогут получить доступ к ним.\n\n'
            'Чтобы найти любимый фильм нажми "🔍 Поиск"')

    await msg.answer(text, reply_markup=kb.get_search_kb())


# принимает видео
@dp.message(lambda msg: msg.video is not None)
async def add_video(msg: Message, state: FSMContext):
    await msg.delete()
    print(msg.video)

    if msg.video.file_name:
        split_title = msg.video.file_name.split('.')
        title = msg.video.file_name[:-1 - len(split_title[-1])].replace('_', ' ')
    else:
        title = 'Нет названия'

    new_video_id = await db.add_video(
        user_id=msg.from_user.id,
        title=title,
        duration=msg.video.duration,
        thumb=msg.video.thumbnail.file_id,
        description=msg.caption,
        entities=proces_entities(msg.caption_entities),
        video_id=msg.video.file_id
    )

    await msg.answer('✅ Видео добавлено')

    text = (f'{title}\n\n'
            f'{msg.caption}')

    await msg.answer_video(
        video=msg.video.file_id,
        caption=text,
        reply_markup=kb.get_edit_video_kb(new_video_id)
    )



