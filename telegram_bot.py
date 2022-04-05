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
import dotenv
import os

dotenv.load_dotenv('keys.env')

token = os.environ.get('API_KEY')
bot = aio.Bot(token)
dp = aio.Dispatcher(bot, storage=MemoryStorage())
conn = mstr_connect.get_connection()


class GetInfo(StatesGroup):
    find_file = State()
    get_screen = State()
    set_filters = State()
    final = State()


@dp.message_handler(commands=['start'], state=None)
async def start_command(message: aio.types.Message):
    await bot.send_message(message.from_user.id,
                           'Введите /search для поиска отчета,\n/help для списка доступных команд')


@dp.message_handler(commands=['help'], state=None)
async def help_command(message: aio.types.Message):
    await bot.send_message(message.from_user.id, f'Список доступных команд:\n /search - поиск отчета')


@dp.message_handler(commands=['search'], state=None)
async def search_command(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введи имя отчета:')
    await GetInfo.find_file.set()


@dp.message_handler(state=GetInfo.find_file)
async def search_file(message: aio.types.Message):
    all_reports = mstr_connect.search_report(conn, message.text)
    all_documents = mstr_connect.search_document(conn, message.text)

    # Отправляем все доступные репорты
    if len(all_reports) != 0:
        all_reports_keyboard = InlineKeyboardMarkup()

        for report in all_reports:
            # Проверка, что файл является репортом, а не кубом или чем-то еще
            if report.subtype == 768:
                report_button = InlineKeyboardButton(report.name, callback_data=f'report_{report.id}')
                all_reports_keyboard.add(report_button)

        await bot.send_message(message.from_user.id, 'Список доступных репортов:', reply_markup=all_reports_keyboard)

    # Отправляем все доступные документы
    if len(all_documents) != 0:
        all_documents_keyboard = InlineKeyboardMarkup()

        for document in all_documents:
            document_button = InlineKeyboardButton(document.name, callback_data=f'document_{document.id}')
            all_documents_keyboard.add(document_button)

        await bot.send_message(message.from_user.id, 'Список доступных документов:',
                               reply_markup=all_documents_keyboard)

    await GetInfo.get_screen.set()


@dp.callback_query_handler(Text(startswith=['report_', 'document_']), state=GetInfo.get_screen)
async def get_screenshot(call: aio.types.CallbackQuery, state: FSMContext):
    # TODO: продумать удаление/изменение inline клавиатуры
    file_type = call.data.split('_')[0]
    file_id = call.data.split('_')[1]

    # создаем страницу в браузере, отправляем скриншот <id пользователя>.png
    # TODO: подумать как лучше: сообщение в чате или answer
    # await bot.edit_message_text('Отправляем скриншот отчета...', chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.answer(text='Отправляем скриншот отчета...', show_alert=True)
    await screenshot.create_page(aio.types.User.get_current().id, {'docID': file_id})
    await screenshot.get_filter_screen(aio.types.User.get_current().id)
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

    '''
    async with state.proxy() as data:
        data['file_type'] = file_type
        data['file_id'] = file_id
    '''


@dp.callback_query_handler(Text(startswith='noFilter'), state=GetInfo.get_screen)
async def no_filter(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
    await state.finish()


@dp.callback_query_handler(Text(startswith='yesFilter'), state=GetInfo.get_screen)
async def get_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await GetInfo.set_filters.set()

    await call.message.delete()

    selectors_multi, selectors_wo_multi = await screenshot.get_selectors(aio.types.User.get_current().id)
    # TODO: подумать над callback_data и в каком виде хранить селекторы
    # отправляем селекторы с мультивыбором
    if len(selectors_multi) != 0:
        selectors_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_multi:
            selectors_multi_button = InlineKeyboardButton(selector, callback_data=f'sel_{selectors_multi[selector]}')
            selectors_multi_keyboard.add(selectors_multi_button)
        await bot.send_message(call.message.chat.id, 'Селекторы с мультивыбором:', reply_markup=selectors_multi_keyboard)

    # отправляем селекторы без мультивыбора
    if len(selectors_wo_multi) != 0:
        selectors_wo_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_wo_multi:
            selectors_wo_multi_button = InlineKeyboardButton(selector, callback_data=f'sel_{selectors_wo_multi[selector]}')
            selectors_wo_multi_keyboard.add(selectors_wo_multi_button)
        await bot.send_message(call.message.chat.id, 'Селекторы без мультивыбора:',
                               reply_markup=selectors_wo_multi_keyboard)

    continue_keyboard = InlineKeyboardMarkup()
    continue_button = InlineKeyboardButton('Продолжить', callback_data='continue')
    continue_keyboard.add(continue_button)
    await bot.send_message(call.message.chat.id, "После выбора селекторов нажмите 'Продолжить'",
                           reply_markup=continue_keyboard)

    '''
    async with state.proxy() as data:
        data['all_selectors'] = await screenshot.get_selectors(aio.types.User.get_current().id)
        data['active_selectors'] = await screenshot.get_selectors(aio.types.User.get_current().id)
        data['final'] = {}
    '''

    '''
    selectors_keyboard = InlineKeyboardMarkup()
    for selector_name in data['active_selectors'].keys():
        if selector_name[0] not in ('S', 's'):
            selector_button = InlineKeyboardButton(selector_name, callback_data='sel,' + selector_name + ',' +
                                                                                data['active_selectors'][
                                                                                    selector_name])
            selectors_keyboard.add(selector_button)

    continue_button = InlineKeyboardButton('Продолжить', callback_data='continue')
    selectors_keyboard.add(continue_button)
    await bot.send_message(call.message.chat.id, 'Выберите селекторы на которые хотите добавить фильтр',
                           reply_markup=selectors_keyboard)
                           '''

    # TODO: дальше код не смотреть, его надо переделать

@dp.callback_query_handler(Text(startswith='sel,'), state=GetInfo.set_filters)
async def add_selector(call: aio.types.CallbackQuery, state: FSMContext):
    selector_name = call.data.split(',')[1]
    ckey = call.data.split(',')[2]
    new_keyboard = InlineKeyboardMarkup()

    await bot.send_message(call.message.chat.id, f'Выбран селектор {selector_name}')

    async with state.proxy() as data:
        data[f'values,{selector_name},{ckey}'] = await screenshot.get_values(aio.types.User.get_current().id, ckey)
        data['active_selectors'].pop(selector_name)
    for s_name in data['active_selectors'].keys():
        if s_name[0] not in ('s', 'S'):
            new_keyboard.add(
                InlineKeyboardButton(s_name, callback_data='sel,' + s_name + ',' + data['active_selectors'][s_name]))
    new_keyboard.add(InlineKeyboardButton('Продолжить', callback_data='continue'))
    await bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=new_keyboard)


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

    await screenshot.get_filter_screen(aio.types.User.get_current().id,
                                       {'docType': data['file_type'], 'filters': filters})

    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile(str(aio.types.User.get_current().id) + '.png'),
                         caption='Скриншот с добавленными фильтрами')
    await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
    await state.finish()


aio.executor.start_polling(dp, on_startup=screenshot.on_startup)
