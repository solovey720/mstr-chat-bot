
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, db, bot

from webdriver.scheduler import scheduler, scheduler_dashboard

from translate import _

# Функция добавления избранного отчета в базу данных
async def add_scheduler(call: CallbackQuery, state: FSMContext):
    print('')
    #scheduler.add_job(scheduler_dashboard, "cron", day_of_week='mon-sun', hour=17, minute=46, misfire_grace_time = None, replace_existing=True, args=[user_id, {'docID': '18C63CAE4B8268E07E3DAEA5E275BCC3', 'path_screenshot':f'{user_id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr', name=f'sec_withsec_withfiltr')
    # file_id = ''
    # async with state.proxy() as data:
    #     language = data.get('language','ru')
    #     file_id = data['file_id']
    #     if data.get('filters', None):
    #         json_string = {file_id: {}}
    #         for selector in data['filters']:
    #             val_list = []
    #             for val in data['filters'][selector]:
    #                 val_list.append(list(val.values())[0])
    #             json_string[file_id].update({selector.split(';')[1]: val_list})
    #         db.concat_favorite(User.get_current().id, json_string)
    #     else:
    #         db.concat_favorite(User.get_current().id, {file_id: None})

    #     await bot.send_message(User.get_current().id, _(language)('added_to_favorite'))
    


def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_scheduler, Text(equals='add_scheduler'),
                                       state=GetInfo.set_filters)
