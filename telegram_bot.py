import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from mstrio.types import ObjectTypes, ObjectSubTypes
import mstr_connect
import aiogram as aio
from pyppeteer import launch
import screenshot
from aiogram.dispatcher.filters.state import StatesGroup, State

#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'0105984311EA440357CD0080EF354C4B','docType': 'document','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))
#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'743FFE22314887C8F2407C9B559ECB4C','docType': 'dossier','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))


token = '5181481316:AAFrV0UNkG7to7AWhwFjFyviQbqHPHH1MtU'
bot = aio.Bot(token)
dp = aio.Dispatcher(bot, storage=MemoryStorage())
conn = mstr_connect.get_connection()



class get_info(StatesGroup):
    find_name = State()
    file_data = State()
    final = State()


@dp.message_handler(commands=['start'])
async def start_message(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введите /search для поиска отчета')
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Нужная кнопка', callback_data='document_A76ADD394EC610BD76FFBCBE03023721'))
    await bot.send_message(message.from_user.id, 'нажми', reply_markup=keyboard)


@dp.message_handler(commands=['search'])
async def start_message(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введи имя отчета:')
    await get_info.find_name.set()


@dp.message_handler(state=get_info.find_name)
async def search_report(message: aio.types.Message, state: FSMContext):
    all_reports = InlineKeyboardMarkup()
    all_documents = InlineKeyboardMarkup()
    async with state.proxy() as data:
        data['find_name'] = message.text
    for report in mstr_connect.search_report(conn, message.text):
        if report.subtype == 768:
            all_reports.add(InlineKeyboardButton(report.name, callback_data=f'report_{report.id}'))
    for document in mstr_connect.search_document(conn, message.text):
        all_documents.add(InlineKeyboardButton(document.name, callback_data=f'document_{document.id}'))
        print(f'document_{document.id}')
    #await state.finish()
    await bot.send_message(message.from_user.id, 'Список доступных репортов:', reply_markup=all_reports)
    await bot.send_message(message.from_user.id, 'Список доступных документов:', reply_markup=all_documents)
    await get_info.file_data.set()


@dp.callback_query_handler(Text(startswith=['report_', 'document_']))
async def get_screenshot(call: aio.types.CallbackQuery, state: FSMContext):
    print(call.data)
    file_type = call.data.split('_')[0]
    file_id = call.data.split('_')[1]

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id+1) if file_type == 'report' else await bot.delete_message(call.message.chat.id, call.message.message_id-1)

    await call.answer('Сейчас будет отправлен скриншот отчета',)

    async with state.proxy() as data:
        data['file_type'] = file_type
        data['file_id'] = file_id
        data['html'] = await screenshot.screenshot_html({'docID': file_id, 'docType': file_type})
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile('example.png'))

    yes_no_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data=f'addFilter'),
                                                 InlineKeyboardButton('No', callback_data='NoFilter'))
    await bot.send_message(call.message.chat.id, 'Хотите добавить фильтр на отчет?', reply_markup=yes_no_keyboard)


@dp.callback_query_handler(Text(startswith='addFilter'))
async def get_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    async with state.proxy() as data:
        data['all_selectors'] = screenshot.get_selectors(data['html'])
        data['active_selectors'] = screenshot.get_selectors(data['html'])
        data['final'] = {}

    if data['file_type'] == 'document':
        selectors_keyboard = InlineKeyboardMarkup()
        for selector_name in data['active_selectors'].keys():
            print('selector_'+selector_name + '_' + data['active_selectors'][selector_name])
            selectors_keyboard.add(InlineKeyboardButton(selector_name, callback_data='selector_'+selector_name + '_' + data['active_selectors'][selector_name]))
        selectors_keyboard.add(InlineKeyboardButton('Продолжить', callback_data='continue'))
        await bot.send_message(call.message.chat.id, 'Выберите селекторы на которые хотите добавить фильтр', reply_markup=selectors_keyboard)


@dp.callback_query_handler(Text(startswith='selector_'))
async def add_selector(call: aio.types.CallbackQuery, state: FSMContext):
    selector_name = call.data.split('_')[1]
    ckey = call.data.split('_')[2]
    new_keyboard = InlineKeyboardMarkup()
    async with state.proxy() as data:
        data[f'values_{selector_name}_{ckey}'] = screenshot.get_values(data['html'], ckey)
        data['active_selectors'].pop(selector_name)
    for s_name in data['active_selectors'].keys():
        new_keyboard.add(InlineKeyboardButton(s_name, callback_data='selector_'+s_name + '_' + data['active_selectors'][s_name]))
    new_keyboard.add(InlineKeyboardButton('Продолжить', callback_data='continue'))
    await bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=new_keyboard)


@dp.callback_query_handler(Text(startswith='continue'))
async def add_values(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        for selector in data.keys():
            if selector.startswith('values'):
                values_keyboard = InlineKeyboardMarkup()
                for key in data[selector]:
                    values_keyboard.add(InlineKeyboardButton(key, callback_data='add_' + selector.split('_')[1] + '_' + data[selector][key]))
                await bot.send_message(call.message.chat.id, 'Выберите значение селектора ' + selector.split('_')[1] + ':', reply_markup=values_keyboard)


@dp.callback_query_handler(Text(startswith='add_'))
async def final_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    selector_id = call.data.split('_')[1]
    value_id = call.data.split('_')[2]
    async with state.proxy() as data:
        data['final'].update({data['all_selectors'][selector_id]: value_id})
    print(data['final'])




aio.executor.start_polling(dp)