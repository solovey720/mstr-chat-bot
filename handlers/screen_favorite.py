
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import db, GetInfo, bot

from webdriver.scheduler import send_filter_screen, create_page

from translate import _


# Функция отправки скриншота отчета из избранного
async def get_screen_favorite(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
        await bot.send_message(call.message.chat.id, _(language)('send_favorite'))
    all_favorites = db.get_favorite(User.get_current().id)
    file_id = call.data.split(':')[1]
    await create_page(User.get_current().id, {'docID': file_id})
    await send_filter_screen(User.get_current().id, {'filters': all_favorites[file_id]}, is_ctlkey=False)
    yes_no_keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(_(language)('yes'), callback_data='yesFilter')
    no_button = InlineKeyboardButton(_(language)('no'), callback_data='noFilter')
    yes_no_keyboard.add(yes_button, no_button)
    await bot.send_message(call.message.chat.id, _(language)('add_filter'), reply_markup=yes_no_keyboard)
    await GetInfo.set_filters.set()


def register_handlers_screen_with_filters(dp: Dispatcher):
    dp.register_callback_query_handler(get_screen_favorite, Text(startswith='fav:'), state="*")
