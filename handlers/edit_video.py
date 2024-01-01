from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


import db
from init import dp, bot
from utils.message_utils import restore_entities
from keayboards import inline_kb as kb


# включает контекст изменение видео
@dp.callback_query(lambda cb: cb.data.startswith('edit_video'))
async def start_edit_video(cb: CallbackQuery, state: FSMContext):
    _, action, video_id = cb.data.split(':')

    await state.set_state('edit_video')
    await state.update_data(data={
        'action': action,
        'video_id': int(video_id),
        'message_id': cb.message.message_id,
        'text': cb.message.caption
    })

    if action == 'title':
        text = 'Отправьте новое название фильма'
    elif action == 'description':
        text = 'Отправьте новое описание фильма'
    else:
        text = 'Error'

    await cb.answer(text, show_alert=True)


# Исправление видео
@dp.message(StateFilter('edit_video'))
async def edit_video(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    await state.clear()

    await db.edit_video(
        video_id=data['video_id'],
        action=data['action'],
        data=msg.text
    )

    print(data['text'])
    print('\n--------------\n')
    text_split = data['text'].split('\n\n')

    text = (f'{text_split[0]}'
            f'{data["text"][len(text_split[0]):]}')

    if data['action'] == 'title':
        text = (f'{msg.text}\n\n'
                f'{data ["text"] [len (text_split [0]):]}')
    elif data['action'] == 'description':
        text = (f'{text_split [0]}\n\n'
                f'{msg.text}')

    await bot.edit_message_caption(
        chat_id=msg.chat.id,
        message_id=data['message_id'],
        caption=text,
        reply_markup=kb.get_edit_video_kb(data['video_id'])
    )
