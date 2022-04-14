from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from create_bot_and_conn import GetInfo


async def add_to_favorite(call: CallbackQuery, state: FSMContext):
    file_id = ''
    async with state.proxy() as data:
        file_id = data['file_id']




def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_to_favorite, Text(equals='add_favorite'),
                                    state=GetInfo.get_screen)
