from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
import mstr_connect
import aiogram as aio
import screenshot
from aiogram.dispatcher.filters.state import StatesGroup, State
import dotenv
import os
from translate import _

dotenv.load_dotenv('keys.env')

token = os.environ.get('API_KEY')
bot = aio.Bot(token)
dp = aio.Dispatcher(bot, storage=MemoryStorage())
conn = mstr_connect.get_connection()


class GetInfo(StatesGroup):
    set_language = State()
    find_file = State()
    get_screen = State()
    set_filters = State()
    final = State()

'''********************************КОМАНДЫ************************************************'''
@dp.message_handler(commands=['language'], state=None)
async def language_command(message: aio.types.Message, state=FSMContext):
    language_keyboard = InlineKeyboardMarkup()
    rus_lang_button = InlineKeyboardButton('rus', callback_data='lang:ru')
    eng_lang_button = InlineKeyboardButton('eng', callback_data='lang:en')
    language_keyboard.add(rus_lang_button, eng_lang_button)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выберите язык\nChoose language',
                           reply_markup=language_keyboard)
    await GetInfo.set_language.set()


@dp.message_handler(commands=['start'], state=None)
async def start_command(message: aio.types.Message):
    language_keyboard = InlineKeyboardMarkup()
    rus_lang_button = InlineKeyboardButton('rus', callback_data='lang:ru')
    eng_lang_button = InlineKeyboardButton('eng', callback_data='lang:en')
    language_keyboard.add(rus_lang_button, eng_lang_button)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выберите язык\n Choose language',
                           reply_markup=language_keyboard)
    await GetInfo.set_language.set()

    print(aio.types.User.get_current())


@dp.callback_query_handler(Text(startswith='lang:'), state=GetInfo.set_language)
async def change_language(call: aio.types.  CallbackQuery, state: FSMContext):
    await call.message.delete()
    language = call.data.split(':')[1]
    async with state.proxy() as data:
        data['language'] = language
        await bot.send_message(call.message.chat.id, text=_(language)('begin'))
    await state.reset_state(with_data=False)


@dp.message_handler(commands=['help'], state=None)
async def help_command(message: aio.types.Message, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
        await bot.send_message(message.from_user.id, _(language)('command_list'))


@dp.message_handler(commands=['search'], state=None)
async def search_command(message: aio.types.Message, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
    await bot.send_message(message.from_user.id, _(language)('file_name'))
    await GetInfo.find_file.set()
    print(aio.types.User.get_current())


@dp.message_handler(state=GetInfo.find_file)
async def search_file(message: aio.types.Message, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        data['selectors_wo_multi'] = {}
        data['selectors_multi'] = {}
        data['filters'] = {}
        data['messages_id'] = {}
        language = data['language']

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

        await bot.send_message(message.from_user.id, _(language)('report_list'), reply_markup=all_reports_keyboard)

    # Отправляем все доступные документы
    if all_documents:
        all_documents_keyboard = InlineKeyboardMarkup()

        for document in all_documents:
            document_button = InlineKeyboardButton(document.name, callback_data=f'document:{document.id}')
            all_documents_keyboard.add(document_button)

        await bot.send_message(message.from_user.id, _(language)('document_list'),
                               reply_markup=all_documents_keyboard)

    await GetInfo.get_screen.set()


@dp.callback_query_handler(Text(startswith=['report:', 'document:']), state=GetInfo.get_screen)
async def send_screenshot(call: aio.types.CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']
    # TODO: продумать удаление/изменение inline клавиатуры
    file_type = call.data.split(':')[0]
    file_id = call.data.split(':')[1]


    # создаем страницу в браузере, отправляем скриншот <id пользователя>.png
    await bot.edit_message_text(_(language)('send_report'), chat_id=call.message.chat.id,
                                message_id=call.message.message_id)
    # await call.answer('Отправляем скриншот отчета...', show_alert=True)
    await screenshot.create_page(aio.types.User.get_current().id, {'docID': file_id})
    await screenshot.get_filter_screen(aio.types.User.get_current().id)
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile(str(aio.types.User.get_current().id) + '.png'))
    os.remove(str(aio.types.User.get_current().id) + '.png')

    if file_type == 'report':
        await bot.send_message(call.message.chat.id, _(language)('type_search'))
        await state.finish()
    else:
        yes_no_keyboard = InlineKeyboardMarkup()
        yes_button = InlineKeyboardButton(_(language)('yes'), callback_data='yesFilter')
        no_button = InlineKeyboardButton(_(language)('no'), callback_data='noFilter')
        yes_no_keyboard.add(yes_button, no_button)
        await bot.send_message(call.message.chat.id, _(language)('add_filter'), reply_markup=yes_no_keyboard)
        await GetInfo.set_filters.set()


@dp.callback_query_handler(Text(startswith='noFilter'), state=GetInfo.set_filters)
async def no_filter(call: aio.types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
        await call.message.delete()
        await bot.send_message(call.message.chat.id, _(language)('type_search'))
    await state.finish()
    await screenshot.close_page(aio.types.User.get_current().id)


@dp.callback_query_handler(Text(startswith='yesFilter'), state=GetInfo.set_filters)
async def get_filters(call: aio.types.CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']
    await call.message.delete()

    selectors_multi, selectors_wo_multi = await screenshot.get_selectors(aio.types.User.get_current().id)

    # отправляем селекторы с мультивыбором
    if selectors_multi:
        selectors_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_multi:
            if selector[0] not in ('S', 's'):
                selectors_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:mult:{selector}')
                selectors_multi_keyboard.add(selectors_multi_button)
                async with state.proxy() as data:
                    data['selectors_multi'].update({selector: selectors_multi[selector]})
        await bot.send_message(call.message.chat.id, _(language)('mult_selectors'),
                               reply_markup=selectors_multi_keyboard)

    # отправляем селекторы без мультивыбора
    if selectors_wo_multi:
        selectors_wo_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_wo_multi:
            if selector[0] not in ('S', 's'):
                selectors_wo_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:womult:{selector}')
                selectors_wo_multi_keyboard.add(selectors_wo_multi_button)
                async with state.proxy() as data:
                    data['selectors_wo_multi'].update({selector: selectors_wo_multi[selector]})
        await bot.send_message(call.message.chat.id, _(language)('wo_mult_selectors'),
                               reply_markup=selectors_wo_multi_keyboard)

    # TODO: подумать над текстом
    send_screen_keyboard = InlineKeyboardMarkup()
    send_screen_button = InlineKeyboardButton(_(language)('get_screen'), callback_data='getScreen')
    send_screen_keyboard.add(send_screen_button)
    await bot.send_message(call.message.chat.id, _(language)('get_screen'), reply_markup=send_screen_keyboard)


@dp.callback_query_handler(Text(startswith='sel:'), state=GetInfo.set_filters)
async def get_values(call: aio.types.CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']

    selector_name = call.data.split(':')[2]
    selector_type = call.data.split(':')[1]
    selector_ctl = ''
    if selector_type == 'mult':
        async with state.proxy() as data:
            selector_ctl = data['selectors_multi'][selector_name]
    else:
        async with state.proxy() as data:
            selector_ctl = data['selectors_wo_multi'][selector_name]

    # добавляем ctl селектора в словарь filters
    async with state.proxy() as data:
        data['active_selector'] = selector_ctl
        data['filters'].update({selector_ctl: []})

    selector_values = await screenshot.get_values(aio.types.User.get_current().id, selector_ctl)
    async with state.proxy() as data:
        data['selector_values'] = selector_values

    if selector_values:
        selector_values_keyboard = InlineKeyboardMarkup()
        for value in selector_values:
            selector_values_button = InlineKeyboardButton(value, callback_data=f'val:{selector_type}:{value}')
            selector_values_keyboard.add(selector_values_button)

        if selector_type == 'mult':
            # await bot.send_message(call.message.chat.id,
            #                       f'Выберите одно или несколько значений для селектора \'{selector_name}\':',
            #                       reply_markup=selector_values_keyboard)
            # TODO: вот тут как
            await bot.edit_message_text(text=_(language)('sel_val_mult').format(selector_name),
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=selector_values_keyboard)
            try:
                await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
                await bot.delete_message(call.message.chat.id, call.message.message_id + 2)
            except Exception as e:
                await bot.delete_message(call.message.chat.id, call.message.message_id + 2)
        else:
            # await bot.send_message(call.message.chat.id,
            #                       f'Выберите одно значение для селектора \'{selector_name}\':',
            #                       reply_markup=selector_values_keyboard)
            await bot.edit_message_text(text=_(language)('sel_val_wo_mult').format(selector_name),
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=selector_values_keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
            async with state.proxy() as data:
                if data['selectors_multi']:
                    await bot.delete_message(call.message.chat.id, call.message.message_id - 1)

        # TODO: подумать над текстом кнопок и сообщения
        choice_keyboard = InlineKeyboardMarkup()
        choose_selector_button = InlineKeyboardButton(_(language)('more_selectors'), callback_data='yesFilter')
        choose_screen_button = InlineKeyboardButton(_(language)('get_screen'), callback_data='getScreen')
        choice_keyboard.add(choose_selector_button, choose_screen_button)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=_(language)('set_sel_val'),
                               reply_markup=choice_keyboard)


@dp.callback_query_handler(Text(equals='getScreen'), state=GetInfo.set_filters)
async def get_screen(call: aio.types.CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']

    filters = {}
    async with state.proxy() as data:
        for sel_ctl in data['filters']:
            sel_list = []
            print(sel_ctl + '---------sel_ctl')
            for dic in data['filters'][sel_ctl]:
                print(dic)
                sel_list.append(list(dic.keys())[0])
            if sel_list:
                filters[sel_ctl] = sel_list

    await bot.send_message(call.message.chat.id, _(language)('send_report'))
    try:
        await screenshot.get_filter_screen(aio.types.User.get_current().id, {'filters': filters})
        await bot.send_photo(chat_id=call.message.chat.id,
                             photo=InputFile(str(aio.types.User.get_current().id) + '.png'))
        os.remove(str(aio.types.User.get_current().id) + '.png')
    except screenshot.errors.TimeoutError as e:
        await bot.send_message(call.message.chat.id, _(language)('no_data'))

    # TODO: подумать над текстом кнопок и сообщений
    choice_keyboard = InlineKeyboardMarkup()
    change_selectors_button = InlineKeyboardButton(_(language)('more_selectors'), callback_data='yesFilter')
    find_another_button = InlineKeyboardButton(_(language)('find_another'), callback_data='findAnother')
    choice_keyboard.add(change_selectors_button, find_another_button)
    await bot.send_message(chat_id=call.message.chat.id, text=_(language)('wtd'), reply_markup=choice_keyboard)


@dp.callback_query_handler(Text(startswith='val'), state=GetInfo.set_filters)
async def add_values(call: aio.types.CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']

    selector_type = call.data.split(':')[1]
    selector_value = ''
    selector_value_name = call.data.split(':')[2]
    selected_values = []

    async with state.proxy() as data:
        selector_value = data['selector_values'][selector_value_name]
        selector_ctl = data['active_selector']
        if selector_type == 'mult':
            data['filters'][selector_ctl].append({selector_value: selector_value_name})
        else:
            data['filters'][selector_ctl] = [{selector_value: selector_value_name}]
        for value_name in data['filters'][selector_ctl]:
            selected_values.append(list(value_name.values())[0])

        choice_keyboard = InlineKeyboardMarkup()
        choose_selector_button = InlineKeyboardButton(_(language)('more_selectors'), callback_data='yesFilter')
        choose_screen_button = InlineKeyboardButton(_(language)('get_screen'), callback_data='getScreen')
        choice_keyboard.add(choose_selector_button, choose_screen_button)

        #TODO: вот тут отже как
        await bot.send_message(chat_id=call.message.chat.id, text=_(language)('selector_set').format(selected_values))


@dp.callback_query_handler(Text(equals='findAnother'), state=GetInfo.set_filters)
async def add_values(call: aio.types.CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']
    await screenshot.close_page(aio.types.User.get_current().id)
    await state.finish()
    await bot.send_message(call.message.chat.id, _(language)('type_search'))


aio.executor.start_polling(dp, on_startup=screenshot.on_startup)
