
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, db


# Функция добавления избранного отчета в базу данных
async def add_to_favorite(call: CallbackQuery, state: FSMContext):
    file_id = ''
    async with state.proxy() as data:
        file_id = data['file_id']
        if data['filters']:
            json_string = {file_id: {}}
            for selector in data['filters']:
                val_list = []
                for val in data['filters'][selector]:
                    val_list.append(list(val.values())[0])
                json_string[file_id].update({selector.split(';')[1]: val_list})
            db.concat_favorite(User.get_current().id, json_string)
        else:
            db.concat_favorite(User.get_current().id, {file_id: None})


def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_to_favorite, Text(equals='add_favorite'),
                                       state=GetInfo.set_filters)
