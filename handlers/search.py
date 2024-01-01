from aiogram.types import Message, InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

import hashlib

import db
from init import dp
from utils.message_utils import restore_entities


# @dp.inline_query
@dp.inline_query()
async def inline(call: InlineQuery):

    results = await db.search_video(call.query)
    input = []
    # len(results)

    for result in results[:8]:
        query_id = hashlib.md5(f'{result.title}'.encode()).hexdigest()
        text = InputTextMessageContent(message_text=f'{result.id}')
        item = InlineQueryResultArticle(
            id=query_id,
            title=f'{result.title}',
            input_message_content=text,
            description=result.description,
            video_duration=result.duration
        )

        input.append(item)

    await call.answer(input, cache_time=60, is_personal=True)


# результат
@dp.message(StateFilter(default_state))
async def get_video(msg: Message):
    await msg.delete()
    video_info = await db.get_video(int(msg.text))

    entities = restore_entities(video_info.entities)
    await msg.answer_video(
        video=video_info.video_id,
        caption=video_info.description,
        caption_entities=entities
    )
