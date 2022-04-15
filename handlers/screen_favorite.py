from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, User

from create_bot_and_conn import db
from screenshot import get_filter_screen

async def get_screen_favorite(call: CallbackQuery):
    all_favorites = db.get_favorite(User.get_current().id)
    file_id = call.data.split(':')[1]
    await get_filter_screen(User.get_current().id)


def register_handlers_screen_with_filters(dp: Dispatcher):
    dp.register_callback_query_handler(get_screen_favorite, Text(startswith='fav:'), state="*")
