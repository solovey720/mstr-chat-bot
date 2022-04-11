from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot_and_conn import GetInfo, conn, bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile, User
from mstr_connect import search_report, search_document
from screenshot import get_filter_screen, create_page
import os
from translate import _
from aiogram import Dispatcher


# @dp.message_handler(state=GetInfo.find_file)
async def search_file(message: Message, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        data['selectors_wo_multi'] = {}
        data['selectors_multi'] = {}
        data['filters'] = {}
        data['messages_id'] = {}
        language = data['language']

    all_reports = search_report(conn, message.text)
    all_documents = search_document(conn, message.text)

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


# @dp.callback_query_handler(Text(startswith=['report:', 'document:']), state=GetInfo.get_screen)
async def send_screenshot_wo_filters(call: CallbackQuery, state: FSMContext):
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
    await create_page(User.get_current().id, {'docID': file_id})
    await get_filter_screen(User.get_current().id)
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile(str(User.get_current().id) + '.png'))
    os.remove(str(User.get_current().id) + '.png')

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


def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_message_handler(search_file, state=GetInfo.find_file)
    dp.register_callback_query_handler(send_screenshot_wo_filters, Text(startswith=['report:', 'document:']), state=GetInfo.get_screen)
