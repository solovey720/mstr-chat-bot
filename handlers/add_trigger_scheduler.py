
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, db, bot, conn

from webdriver.scheduler import scheduler, scheduler_dashboard

from mstr_connect import get_document_name_by_id

from translate import _



# Функция добавления подписки
async def add_trigger_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    #######################
    triggers_list = db.get_triggers()
    triggers_keyboard = InlineKeyboardMarkup()
    for trigger in triggers_list:
        triggers_keyboard.row(InlineKeyboardButton(trigger, callback_data=f'create_trigger_sch:{trigger}'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('choose_trigger'), reply_markup=triggers_keyboard)


#создание подписки
async def create_trigger_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    trigger_name = call.data.split(':')[1]
    async with state.proxy() as data:
        file_id = data['file_id']
        filters = {}
        if data.get('filters', None):
            for selector in data['filters']:
                val_list = []
                for val in data['filters'][selector]:
                    val_list.append(list(val.values())[0])
                filters = {**filters, **{selector.split(';')[1]: val_list}}
        db.insert_trigger_scheduler(trigger_name, User.get_current().id, file_id, filters, get_document_name_by_id(conn, file_id))
        # scheduler.add_job(scheduler_dashboard, "cron", day_of_week=(','.join(data['days'])), hour=data['time']['hour'], minute=data['time']['minute'], misfire_grace_time = None, replace_existing=True, args=[User.get_current().id, {'docID': file_id, 'path_screenshot':f'{User.get_current().id}_{file_id}.png','filters': filters}],id=f'{User.get_current().id}_{file_id}', name=f'{file_id}')
        await bot.send_message(User.get_current().id, _(User.get_current().id)('scheduler_created'))



async def info_about_trigger_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    scheduler_id = call.data.split(':')[1]
    subscription_keyboard = InlineKeyboardMarkup()
    subscription_keyboard.add(InlineKeyboardButton( _(User.get_current().id)('info_scheduler'), callback_data=f'info_trigger_sch:{scheduler_id}'))
    subscription_keyboard.add(InlineKeyboardButton( _(User.get_current().id)('delete_scheduler'), callback_data=f'delete_trigger_sch:{scheduler_id}'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('info_about_scheduler'), reply_markup=subscription_keyboard)


async def info_trigger_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    scheduler_id = call.data.split(':')[1]
    scheduler_info = db.get_truggers_by_id(scheduler_id)
    await bot.send_message(User.get_current().id, _(User.get_current().id)('info_about_trigger_scheduler').format(scheduler_info['document_name'], scheduler_info['trigger_name'], scheduler_info['date_last_update']))


async def delete_trigger_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    scheduler_id = call.data.split(':')[1]
    db.delete_trigger_scheduler(scheduler_id)
    await bot.send_message(User.get_current().id, _(User.get_current().id)('successfully_deleted'))

    

def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_trigger_scheduler, Text(equals='add_trigger_sch'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(create_trigger_scheduler, Text(startswith='create_trigger_sch:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(info_about_trigger_scheduler, Text(startswith='info_about_trigger_sch:'), state='*')
    dp.register_callback_query_handler(info_trigger_scheduler, Text(startswith='info_trigger_sch:'), state='*')
    dp.register_callback_query_handler(delete_trigger_scheduler, Text(startswith='delete_trigger_sch:'), state='*')
    