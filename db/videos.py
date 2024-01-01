import sqlalchemy as sa
import typing as t
import logging

# from sqlalchemy.sql import func
from datetime import datetime, date, timedelta

from init import TZ, log_error
from db.base import METADATA, begin_connection


class VideoRow(t.Protocol):
    id: int
    create_at: datetime
    user_id: int
    title: str
    season: int
    episode: int
    duration: int
    thumb: str
    description: str
    entities: str
    video_id: str


VideoTable = sa.Table(
    'video',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('create_at', sa.DateTime(timezone=True), default=sa.func.now()),
    sa.Column('user_id', sa.BigInteger()),
    sa.Column('type', sa.String(255)),
    sa.Column('title', sa.String(255)),
    sa.Column('season', sa.Integer),
    sa.Column('episode', sa.Integer),
    sa.Column('duration', sa.Integer),
    sa.Column('thumb', sa.String(255)),
    sa.Column('description', sa.Text),
    sa.Column('entities', sa.Text),
    sa.Column('video_id', sa.String(255))
)


# добавляет видео
async def add_video(
        user_id: int,
        title: str,
        description: str,
        duration: int,
        thumb: str,
        entities: str,
        video_id: str
) -> int:
    payload = dict(
        create_at=datetime.now(TZ),
        user_id=user_id,
        type='movie',
        title=title,
        description=description,
        duration=duration,
        thumb=thumb,
        entities=entities,
        video_id=video_id
    )

    async with begin_connection() as conn:
        result = await conn.execute(VideoTable.insert().values(payload))

    return result.lastrowid


# поиск по названию фильма
async def search_video(title_query: str) -> tuple[VideoRow]:
    query = VideoTable.select().where(VideoTable.c.title.like (f'%{title_query}%'))
    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


# Возвращает фильм по id
async def get_video(video_id: int) -> VideoRow:
    async with begin_connection() as conn:
        result = await conn.execute(VideoTable.select().where(VideoTable.c.id == video_id))
    return result.first()


# обновляет данные видео
async def edit_video(video_id: int, action: str, data: str) -> None:
    query = VideoTable.update().where(VideoTable.c.id == video_id)

    if action == 'title':
        query = query.values(title=data)
    elif action == 'description':
        query = query.values (description=data)

    async with begin_connection() as conn:
        await conn.execute(query)


