from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, bot
from aiogram.types import CallbackQuery, User, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from translate import _
from screenshot import get_filter_screen
import os
from screenshot import errors
from aiogram import Dispatcher


# @dp.callback_query_handler(Text(equals='getScreen'), state=GetInfo.set_filters)
async def get_screen(call: CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']

    filters = {}
    async with state.proxy() as data:
        print(data)
        for sel_ctl in data['filters']:
            sel_list = []
            print(sel_ctl + '---------sel_ctl')
            for dic in data['filters'][sel_ctl]:
                print(dic)
                sel_list.append(list(dic.keys())[0])
            if sel_list:
                filters[sel_ctl.split(';')[0]] = sel_list

    await bot.send_message(call.message.chat.id, _(language)('send_report'))
    try:
        await get_filter_screen(User.get_current().id, {'filters': filters})
        await bot.send_photo(chat_id=call.message.chat.id,
                             photo=InputFile(str(User.get_current().id) + '.png'))
        os.remove(str(User.get_current().id) + '.png')
    except errors.TimeoutError as e:
        await bot.send_message(call.message.chat.id, _(language)('no_data'))

    # TODO: подумать над текстом кнопок и сообщений
    choice_keyboard = InlineKeyboardMarkup(row_width=2)
    change_selectors_button = InlineKeyboardButton(_(language)('more_selectors'), callback_data='yesFilter')
    find_another_button = InlineKeyboardButton(_(language)('find_another'), callback_data='findAnother')
    add_to_favorite = InlineKeyboardButton('Добавить в избранное', callback_data='add_favorite')
    choice_keyboard.add(change_selectors_button, find_another_button, add_to_favorite)
    await bot.send_message(chat_id=call.message.chat.id, text=_(language)('wtd'), reply_markup=choice_keyboard)


def register_handlers_screen_with_filters(dp: Dispatcher):
    dp.register_callback_query_handler(get_screen, Text(equals='getScreen'), state=GetInfo.set_filters)