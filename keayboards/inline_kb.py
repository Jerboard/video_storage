from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


# поиск
def get_search_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Поиск', switch_inline_query_current_chat='')
    return kb.as_markup()


# редактировать видео
def get_edit_video_kb(video_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Изменить название', callback_data=f'edit_video:title:{video_id}')
    kb.button(text='Изменить описание', callback_data=f'edit_video:description:{video_id}')
    kb.adjust(1)
    return kb.as_markup()