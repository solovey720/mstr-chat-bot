
from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.dispatcher import FSMContext

from create_bot_and_conn import bot, GetInfo, db

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
    await GetInfo.find_file.set()


# Команда для вывода всех избранных отчетов
async def favorite_command(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    all_favorites = db.get_favorite(User.get_current().id)
    all_favorites_keyboard = InlineKeyboardMarkup()
    for file_id in all_favorites:
        file_id_button = InlineKeyboardButton(text=file_id, callback_data='fav:'+file_id)
        all_favorites_keyboard.add(file_id_button)

    await bot.send_message(message.from_user.id, _(message.from_user.id)('favorites'), reply_markup=all_favorites_keyboard)


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(language_command, commands=['language'], state="*")
    dp.register_message_handler(start_command, commands=['start'], state="*")
    dp.register_message_handler(help_command, commands=['help'], state="*")
    dp.register_message_handler(search_command, commands=['search'], state="*")
    dp.register_message_handler(favorite_command, commands=['favorite'], state="*")
