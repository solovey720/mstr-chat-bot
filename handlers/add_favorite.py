from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, User

from create_bot_and_conn import GetInfo
from create_bot_and_conn import db

async def add_to_favorite(call: CallbackQuery, state: FSMContext):
    file_id = ''
    print('в нужной функции')
    async with state.proxy() as data:
        file_id = data['file_id']
        if data['filters']:
            json_string = {file_id: {}}
            for selector in data['filters']:
                val_list = []
                for val in data['filters'][selector]:
                    val_list.append(list(val.values())[0])
                    print(list(val.values())[0])
                json_string[file_id].update({selector.split(';')[1]: val_list})
            print(json_string)
            db.concat_favorite(User.get_current().id, json_string)
            print('после')
            print(db.get_favorite(User.get_current().id))
        else:
            db.concat_favorite(User.get_current().id, {file_id: None})
            print(db.get_favorite(User.get_current().id))


def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_to_favorite, Text(equals='add_favorite'),
                                       state=GetInfo.set_filters)
