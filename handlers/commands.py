
from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.dispatcher import FSMContext

from create_bot_and_conn import bot, GetInfo, db, conn

from webdriver.scheduler import get_user_jobs, close_browser

from mstr_connect import get_document_name_by_id


from translate import _


# Команда для смены языка
async def language_command(message: Message):
    language_keyboard = InlineKeyboardMarkup()
    rus_lang_button = InlineKeyboardButton('rus', callback_data='lang:ru')
    eng_lang_button = InlineKeyboardButton('eng', callback_data='lang:en')
    language_keyboard.add(rus_lang_button, eng_lang_button)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выберите язык\nChoose language',
                           reply_markup=language_keyboard)
    await GetInfo.set_language.set()


# Команда запуска бота
async def start_command(message: Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['selectors_wo_multi'] = {}
    #     data['selectors_multi'] = {}
    #     data['filters'] = {}

    db.insert_new_user(User.get_current().id)
    await bot.send_message(message.from_user.id, text=_(message.from_user.id)('begin'))
    


# Команда помощи
async def help_command(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, _(message.from_user.id)('command_list'))


# Команда для поиска отчета
async def search_command(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, _(message.from_user.id)('file_name'))
    await close_browser(message.from_user.id)
    await GetInfo.find_file.set()


# Команда для вывода всех избранных отчетов
async def favorite_command(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    all_favorites = db.get_favorite(User.get_current().id)
    if all_favorites:
        all_favorites_keyboard = InlineKeyboardMarkup()
        for file_id in all_favorites:
            file_id_button = InlineKeyboardButton(text=get_document_name_by_id(conn, file_id), callback_data='fav:'+file_id)
            all_favorites_keyboard.add(file_id_button)
        await bot.send_message(message.from_user.id, _(message.from_user.id)('favorites'), reply_markup=all_favorites_keyboard)
    else:
        await bot.send_message(message.from_user.id, _(message.from_user.id)('list_of_favorite_is_empty'))


# Команда для вывода всех избранных отчетов
async def delete_favorite_command(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    all_favorites = db.get_favorite(User.get_current().id)
    if all_favorites:
        all_favorites_keyboard = InlineKeyboardMarkup()
        for file_id in all_favorites:
            file_id_button = InlineKeyboardButton(text=get_document_name_by_id(conn, file_id), callback_data='delete_favorite:'+file_id)
            all_favorites_keyboard.add(file_id_button)
        await bot.send_message(message.from_user.id, _(message.from_user.id)('click_to_delete'), reply_markup=all_favorites_keyboard)
    else:
        await bot.send_message(message.from_user.id, _(message.from_user.id)('list_of_favorite_is_empty'))


#список всех подписок
async def subscription_command(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    all_subscription = get_user_jobs(str(message.from_user.id))
    all_subscription_keyboard = InlineKeyboardMarkup()
    if all_subscription:
        for job in all_subscription:
            all_subscription_keyboard.add(InlineKeyboardButton(text=get_document_name_by_id(conn, job.name), callback_data=f'info_about_scheduler:{job.id}'))
        await bot.send_message(message.from_user.id, _(message.from_user.id)('list_of_scheduler'), reply_markup=all_subscription_keyboard)
    else:
        await bot.send_message(message.from_user.id, _(message.from_user.id)('list_of_scheduler_is_empty'))

#для тестов
async def test_command(message: Message, state: FSMContext):
    #all_reports = search_document_by_id(conn, '8CD564B54D2ED4AFD358F3853610D647')
    pass
    #print(all_reports)


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(language_command, commands=['language'], state="*")
    dp.register_message_handler(start_command, commands=['start'], state="*")
    dp.register_message_handler(help_command, commands=['help'], state="*")
    dp.register_message_handler(search_command, commands=['search'], state="*")
    dp.register_message_handler(favorite_command, commands=['favorite'], state="*")
    dp.register_message_handler(delete_favorite_command, commands=['delete_favorite'], state="*")
    dp.register_message_handler(subscription_command, commands=['subscription'], state="*")
    dp.register_message_handler(test_command, commands=['QWERTY123'], state="*")
