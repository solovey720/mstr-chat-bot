from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from create_bot_and_conn import bot, GetInfo, db
from translate import _
from create_bot_and_conn import db


# @dp.message_handler(commands=['language'], state=None)
async def language_command(message: Message):
    language_keyboard = InlineKeyboardMarkup()
    rus_lang_button = InlineKeyboardButton('rus', callback_data='lang:ru')
    eng_lang_button = InlineKeyboardButton('eng', callback_data='lang:en')
    language_keyboard.add(rus_lang_button, eng_lang_button)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выберите язык\nChoose language',
                           reply_markup=language_keyboard)
    await GetInfo.set_language.set()


# @dp.message_handler(commands=['start'], state=None)
async def start_command(message: Message, state: FSMContext):
    db.insert_new_user(User.get_current().id)

    language_keyboard = InlineKeyboardMarkup()
    rus_lang_button = InlineKeyboardButton('rus', callback_data='lang:ru')
    eng_lang_button = InlineKeyboardButton('eng', callback_data='lang:en')
    language_keyboard.add(rus_lang_button, eng_lang_button)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выберите язык\n Choose language',
                           reply_markup=language_keyboard)
    await GetInfo.set_language.set()

    print(User.get_current())
    db.show_all()


# @dp.message_handler(commands=['help'], state=None)
async def help_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
        await bot.send_message(message.from_user.id, _(language)('command_list'))


# @dp.message_handler(commands=['search'], state=None)
async def search_command(message: Message, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
    await bot.send_message(message.from_user.id, _(language)('file_name'))
    await GetInfo.find_file.set()
    print(User.get_current())


async def favorite_command(message: Message, state: FSMContext):
    all_favorites = db.get_favorite(User.get_current().id)
    all_favorites_keyboard = InlineKeyboardMarkup()
    for file_id in all_favorites:
        file_id_button = InlineKeyboardButton(text=file_id, callback_data='fav:'+file_id)
        all_favorites_keyboard.add(file_id_button)

    await bot.send_message(message.from_user.id, 'Ваши любимчики:', reply_markup=all_favorites_keyboard)


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(language_command, commands=['language'], state=None)
    dp.register_message_handler(start_command, commands=['start'], state="*")
    dp.register_message_handler(help_command, commands=['help'], state=None)
    dp.register_message_handler(search_command, commands=['search'], state=None)
    dp.register_message_handler(favorite_command, commands=['favorite'], state=None)
