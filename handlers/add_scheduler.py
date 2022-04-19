
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, db, bot

from webdriver.scheduler import scheduler, scheduler_dashboard

from translate import _

# Функция добавления избранного отчета в базу данных
async def add_scheduler(call: CallbackQuery, state: FSMContext):
    #scheduler.add_job(scheduler_dashboard, "cron", day_of_week='mon-sun', hour=11, minute=46, misfire_grace_time = None, replace_existing=True, args=[User.get_current().id, {'docID': file_id, 'path_screenshot':f'{User.get_current().id}_{file_id}.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{User.get_current().id}_{file_id}', name=f'{file_id}')
    file_id = ''
    filters = {}
    async with state.proxy() as data:
        file_id = data['file_id']
        if data.get('filters', None):
            #json_string = {file_id: {}}
            for selector in data['filters']:
                val_list = []
                for val in data['filters'][selector]:
                    val_list.append(list(val.values())[0])
                filters = filters | {selector.split(';')[1]: val_list}
                #json_string[file_id].update({selector.split(';')[1]: val_list})
        #     db.concat_favorite(User.get_current().id, json_string)
        # else:
        #     db.concat_favorite(User.get_current().id, {file_id: None})
        scheduler.add_job(scheduler_dashboard, "cron", day_of_week='mon-fri', hour=18, minute=0, misfire_grace_time = None, replace_existing=True, args=[User.get_current().id, {'docID': file_id, 'path_screenshot':f'{User.get_current().id}_{file_id}.png', 'security': db.get_security(User.get_current().id),'filters': filters}],id=f'{User.get_current().id}_{file_id}', name=f'{file_id}')

        await bot.send_message(User.get_current().id, _(User.get_current().id)('added_to_scheduler'))
    


def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_scheduler, Text(equals='add_scheduler'),
                                       state=GetInfo.set_filters)
