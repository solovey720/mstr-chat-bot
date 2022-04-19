from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, conn, bot, db

from mstr_connect import search_report, search_document

from webdriver.scheduler import send_filter_screen, create_page

from translate import _


# Выводим список доступных отчетов
async def search_file(message: Message, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data.get('language','ru')
        data['selectors_wo_multi'] = {}
        data['selectors_multi'] = {}
        data['filters'] = {}

    all_reports = search_report(conn, message.text)
    all_documents = search_document(conn, message.text)

    if not(all_reports or all_documents):
        await bot.send_message(message.from_user.id, _(language)('nothing_found'))
        return

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


# Отправляем скрин без фильтров
async def send_screenshot_wo_filters(call: CallbackQuery, state: FSMContext):
    #TODO: продумать логику для репорта

    file_type = call.data.split(':')[0]
    file_id = call.data.split(':')[1]

    language = ''
    async with state.proxy() as data:
        language = data.get('language','ru')
        data['file_id'] = file_id

    # создаем страницу в браузере, отправляем скриншот <id пользователя>.png
    await bot.edit_message_text(_(language)('send_report'), chat_id=call.message.chat.id,
                                message_id=call.message.message_id)
    # await call.answer('Отправляем скриншот отчета...', show_alert=True)
    await create_page(User.get_current().id, {'docID': file_id, 'headless': True})
    try:
        await send_filter_screen(User.get_current().id, {'security': db.get_security(User.get_current().id)})
    except KeyError as e:
        if e.args[0] == 'S_security':
            await bot.send_message(call.message.chat.id, _(language)('security_key_error'))
            await bot.send_message(call.message.chat.id, _(language)('file_name'))
            await GetInfo.find_file.set()
            return

    if file_type == 'report':
        await bot.send_message(call.message.chat.id, _(language)('type_search'))
        await state.finish()
    else:
        yes_no_keyboard = InlineKeyboardMarkup(row_width=1)
        yes_button = InlineKeyboardButton(_(language)('yes'), callback_data='yesFilter')
        no_button = InlineKeyboardButton(_(language)('no'), callback_data='noFilter')
        add_to_favorite = InlineKeyboardButton(_(language)('add_to_favorite'), callback_data='add_favorite')
        add_scheduler = InlineKeyboardButton(_(language)('add_scheduler'), callback_data='add_scheduler')
        yes_no_keyboard.row(yes_button, no_button)
        yes_no_keyboard.add(add_to_favorite, add_scheduler)
        await bot.send_message(call.message.chat.id, _(language)('add_filter'), reply_markup=yes_no_keyboard)
        await GetInfo.set_filters.set()


def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_message_handler(search_file, state=GetInfo.find_file)
    dp.register_callback_query_handler(send_screenshot_wo_filters, Text(startswith=['report:', 'document:']),
                                       state=GetInfo.get_screen)
