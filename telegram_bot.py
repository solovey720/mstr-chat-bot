import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
#from scheduler import scheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from mstrio.types import ObjectTypes, ObjectSubTypes
import mstr_connect
from create_bot_and_conn import *
from pyppeteer import launch
###################
#from webdriver.screenshot import *
from webdriver.scheduler import *
##########################
from aiogram.dispatcher.filters.state import StatesGroup, State

import json
from translate import _
import dotenv
import os
import aiogram as aio
import asyncio
# dotenv.load_dotenv('keys.env')



# dp = aio.Dispatcher(bot, storage=MemoryStorage())
#conn = mstr_connect.get_connection()


# class GetInfo(StatesGroup):
#     find_file = State()
#     get_screen = State()
#     set_filters = State()
#     final = State()

#sem = asyncio.Semaphore(1)

@dp.message_handler(commands=['start'], state=None)
async def start_command(message: aio.types.Message):
    print('s')
    
    user_id = aio.types.User.get_current().id
    
    #scheduler.add_job(screenshot.click_all_pages,  "interval", seconds=1, replace_existing=True, id=f'{user_id}_click', name='click')
    #scheduler.add_job(scheduler_dashboard,  "interval", seconds=60, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr1.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr1', name='sec_withsec_withfiltr1')
    
    #for i in range (15):
        #scheduler.add_job(semaphore_sched,  "cron",max_instances=1, day_of_week='mon-sun', hour=14, minute=51, misfire_grace_time = None, replace_existing=True, args=[sem, user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr{i}.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr{i}', name=f'sec_withsec_withfiltr{i}')
    scheduler.add_job(scheduler_dashboard, "cron", day_of_week='mon-sun', hour=15, minute=44, misfire_grace_time = None, replace_existing=True, args=[user_id, {'docID': '18C63CAE4B8268E07E3DAEA5E275BCC3', 'path_screenshot':f'{user_id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr', name=f'sec_withsec_withfiltr')
    print('create')
    #scheduler.add_job(scheduler_dashboard,  "cron", day_of_week='mon-sun', hour=12, minute=40, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr1.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr1', name='sec_withsec_withfiltr1')
    # scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr21.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr21', name='sec_withsec_withfiltr12')
    # scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr31.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr31', name='sec_withsec_withfiltr13')
    # scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr41.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr41', name='sec_withsec_withfiltr14')
    # scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr51.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr51', name='sec_withsec_withfiltr15')
    # scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr61.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr61', name='sec_withsec_withfiltr16')
    #scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr', name='sec_withsec_withfiltr')
    '''
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[5, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr2', name='sec_withsec_withfiltr2')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[6, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr3', name='sec_withsec_withfiltr3')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[7, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr4', name='sec_withsec_withfiltr4')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[8, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr5', name='sec_withsec_withfiltr5')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[9, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr6', name='sec_withsec_withfiltr6')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[10, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr7', name='sec_withsec_withfiltr7')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[11, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr8', name='sec_withsec_withfiltr8')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[12, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr9', name='sec_withsec_withfiltr9')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[2, { 'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withfiltr', name='sec_withfiltr')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[3, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER']}],id=f'{user_id}_sec_withsec', name='sec_withsec')
    scheduler.add_job(send_sched_photo,  "interval", seconds=1, replace_existing=True, args=[4],id=f'{user_id}_sec', name='sec')
    print(get_user_jobs(str(user_id)))
    print('f')
    '''
    #scheduler.add_job(screenshot.create_page,  "interval", seconds=3, replace_existing=True, args=[aio.types.User.get_current().id,{'docID': 'EA706ACB43C4530927380DB3B07E0889'}],id='2')
    #print('sched')
    #await screenshot.create_page(aio.types.User.get_current().id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'})
    #await screenshot.get_filter_screen(aio.types.User.get_current().id)
    #await bot.send_photo(chat_id=aio.types.User.get_current().id, photo=InputFile(str(aio.types.User.get_current().id) + '.png'))



@dp.message_handler(commands=['help'], state=None)
async def help_command(message: aio.types.Message):
    print('hs')
    await create_page(aio.types.User.get_current().id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'})
    await send_filter_screen(aio.types.User.get_current().id)
    print('hf')


aio.executor.start_polling(dp)#, on_startup=on_startup)
exit()
@dp.message_handler(commands=['search'], state=None)
async def search_command(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введи имя отчета:')
    await GetInfo.find_file.set()


@dp.message_handler(state=GetInfo.find_file)
async def search_file(message: aio.types.Message):
    all_reports = mstr_connect.search_report(conn, message.text)
    all_documents = mstr_connect.search_document(conn, message.text)

    # Отправляем все доступные репорты
    if all_reports:
        all_reports_keyboard = InlineKeyboardMarkup()

        for report in all_reports:
            # Проверка, что файл является репортом, а не кубом или чем-то еще
            if report.subtype == 768:
                report_button = InlineKeyboardButton(report.name, callback_data=f'report:{report.id}')
                all_reports_keyboard.add(report_button)

        await bot.send_message(message.from_user.id, 'Список доступных репортов:', reply_markup=all_reports_keyboard)

    # Отправляем все доступные документы
    if all_documents:
        all_documents_keyboard = InlineKeyboardMarkup()

        for document in all_documents:
            document_button = InlineKeyboardButton(document.name, callback_data=f'document:{document.id}')
            all_documents_keyboard.add(document_button)

        await bot.send_message(message.from_user.id, 'Список доступных документов:',
                               reply_markup=all_documents_keyboard)

    await GetInfo.get_screen.set()


@dp.callback_query_handler(Text(startswith=['report:', 'document:']), state=GetInfo.get_screen)
async def send_screenshot(call: aio.types.CallbackQuery, state: FSMContext):
    # TODO: продумать удаление/изменение inline клавиатуры
    file_type = call.data.split(':')[0]
    file_id = call.data.split(':')[1]

    # создаем страницу в браузере, отправляем скриншот <id пользователя>.png
    # TODO: подумать как лучше: сообщение в чате или answer
    # await bot.edit_message_text('Отправляем скриншот отчета...', chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.answer(text='Отправляем скриншот отчета...', show_alert=True)
    #await scheduler.create_page(aio.types.User.get_current().id, {'docID': file_id})
    #await scheduler.get_filter_screen(aio.types.User.get_current().id)
    await create_page(aio.types.User.get_current().id, {'docID': file_id})
    await get_filter_screen(aio.types.User.get_current().id)

    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile(str(aio.types.User.get_current().id) + '.png'))

    if file_type == 'report':
        await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
        await state.finish()
    else:
        yes_no_keyboard = InlineKeyboardMarkup()
        yes_button = InlineKeyboardButton('Да', callback_data='yesFilter')
        no_button = InlineKeyboardButton('Нет', callback_data='noFilter')
        yes_no_keyboard.add(yes_button, no_button)
        await bot.send_message(call.message.chat.id, 'Хотите добавить фильтр на отчет?', reply_markup=yes_no_keyboard)


@dp.callback_query_handler(Text(startswith='noFilter'), state=GetInfo.get_screen)
async def no_filter(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
    await state.finish()


@dp.callback_query_handler(Text(startswith='yesFilter'), state=GetInfo.get_screen)
async def get_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await GetInfo.set_filters.set()

    await call.message.delete()

    #selectors_multi, selectors_wo_multi = await scheduler.get_selectors(aio.types.User.get_current().id)
    selectors_multi, selectors_wo_multi = await get_selectors(aio.types.User.get_current().id)

    # отправляем селекторы с мультивыбором
    if selectors_multi:
        async with state.proxy() as data:
            data['selectors_multi'] = {}
        selectors_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_multi:
            if selector[0] not in ('S', 's'):
                selectors_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:mult:{selector}')
                selectors_multi_keyboard.add(selectors_multi_button)
                async with state.proxy() as data:
                    data['selectors_multi'].update({selector: selectors_multi[selector]})
        await bot.send_message(call.message.chat.id, 'Селекторы с мультивыбором:',
                               reply_markup=selectors_multi_keyboard)

    # отправляем селекторы без мультивыбора
    if selectors_wo_multi:
        async with state.proxy() as data:
            data['selectors_wo_multi'] = {}
        selectors_wo_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_wo_multi:
            if selector[0] not in ('S', 's'):
                selectors_wo_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:womult:{selector}')
                selectors_wo_multi_keyboard.add(selectors_wo_multi_button)
                async with state.proxy() as data:
                    data['selectors_wo_multi'].update({selector: selectors_wo_multi[selector]})
        await bot.send_message(call.message.chat.id, 'Селекторы без мультивыбора:',
                               reply_markup=selectors_wo_multi_keyboard)


@dp.callback_query_handler(Text(startswith='sel:'), state=GetInfo.set_filters)
async def get_values(call: aio.types.CallbackQuery, state: FSMContext):
    selector_name = call.data.split(':')[2]
    selector_type = call.data.split(':')[1]
    selector_ctl = ''
    if selector_type == 'mult':
        async with state.proxy() as data:
            selector_ctl = data['selectors_multi'][selector_name]
    else:
        async with state.proxy() as data:
            selector_ctl = data['selectors_wo_multi'][selector_name]

    #selector_values = await scheduler.get_values(aio.types.User.get_current().id, selector_ctl)
    selector_values = await get_values(aio.types.User.get_current().id, selector_ctl)

    if selector_values:
        selector_values_keyboard = InlineKeyboardMarkup()
        for value in selector_values:
            print(value)
            selector_values_button = InlineKeyboardButton(value, callback_data=f'val_{value}')
            selector_values_keyboard.add(selector_values_button)

        await bot.send_message(call.message.chat.id, f'Выберите значения для {selector_type} селектора \'{selector_name}\':',
                               reply_markup=selector_values_keyboard)



# TODO: ниже не смотреть

@dp.callback_query_handler(Text(equals='continue'), state=GetInfo.set_filters)
async def add_values(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        for selector in data.keys():
            if selector.startswith('values'):
                values_keyboard = InlineKeyboardMarkup(row_width=2)
                # print(data[selector].keys())
                c = 0
                for key in data[selector]:
                    if c <= 50:
                        values_keyboard.insert(InlineKeyboardButton(key, callback_data='add,' + selector.split(',')[
                            1] + ',' + data[selector][key]))
                    else:
                        break
                    c += 1
                await bot.send_message(call.message.chat.id,
                                       'Выберите значение селектора ' + selector.split(',')[1] + ':',
                                       reply_markup=values_keyboard)
    await bot.send_message(call.message.chat.id, 'После выбора нужных селекторов нажмите \'Продолжить\':',
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton('Продолжить', callback_data='continue2')))


@dp.callback_query_handler(Text(startswith='add,'), state=GetInfo.set_filters)
async def final_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    print(call.data)

    selector_id = call.data.split(',')[1]
    value_id = call.data.split(',')[2]
    async with state.proxy() as data:
        data['final'].update({data['all_selectors'][selector_id]: value_id})

    selector_ident = ''
    for key in data['final']:
        if data['final'][key] == value_id:
            selector_ident = key

    value_name = ''
    for key in data[f"values,{selector_id},{selector_ident}"]:
        if data[f"values,{selector_id},{selector_ident}"][key] == value_id:
            value_name = key

    await bot.send_message(call.message.chat.id, f"Селектор \'{selector_id}\': {value_name}")

    # print(data)
    # print(data['final'])


@dp.callback_query_handler(Text(equals='continue2'), state=GetInfo.set_filters)
async def screen_with_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, 'Отправляем скриншот с наложенными фильтрами...')
    filters = {}
    async with state.proxy() as data:
        for ctlKey in data['final'].keys():
            filters[ctlKey] = data['final'][ctlKey]

    #await scheduler.get_filter_screen(aio.types.User.get_current().id,
    #                                   {'docType': data['file_type'], 'filters': filters})
    await get_filter_screen(aio.types.User.get_current().id,
                                       {'docType': data['file_type'], 'filters': filters})

    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile(str(aio.types.User.get_current().id) + '.png'),
                         caption='Скриншот с добавленными фильтрами')
    await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
    await state.finish()


aio.executor.start_polling(dp, on_startup=on_startup)
