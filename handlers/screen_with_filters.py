
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, bot, db

from translate import _

from webdriver.scheduler import send_filter_screen, errors


# Функция отправки скриншота с фильтрами
async def get_screen(call: CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data.get('language','ru')

    filters = {}
    async with state.proxy() as data:
        for sel_ctl in data['filters']:
            sel_list = []
            for dic in data['filters'][sel_ctl]:
                sel_list.append(list(dic.keys())[0])
            if sel_list:
                filters[sel_ctl.split(';')[0]] = sel_list

    await bot.send_message(call.message.chat.id, _(language)('send_report'))
    try:
        await send_filter_screen(User.get_current().id, {'filters': filters, 'security': db.get_security(User.get_current().id)})
    except errors.TimeoutError:
        await bot.send_message(call.message.chat.id, _(language)('no_data'))
    except KeyError as e:
        if e.args[0] == 'S_security':
            await bot.send_message(call.message.chat.id, _(language)('security_key_error'))
            await bot.send_message(call.message.chat.id, _(language)('file_name'))
            await GetInfo.find_file.set()
            return

    # TODO: подумать над текстом кнопок и сообщений
    choice_keyboard = InlineKeyboardMarkup(row_width=1)
    change_selectors_button = InlineKeyboardButton(_(language)('more_selectors'), callback_data='yesFilter')
    find_another_button = InlineKeyboardButton(_(language)('find_another'), callback_data='findAnother')
    add_to_favorite = InlineKeyboardButton(_(language)('add_to_favorite'), callback_data='add_favorite')
    add_scheduler = InlineKeyboardButton(_(language)('add_scheduler'), callback_data='add_scheduler')
    choice_keyboard.row(change_selectors_button, find_another_button)
    choice_keyboard.add(add_to_favorite, add_scheduler)
    await bot.send_message(chat_id=call.message.chat.id, text=_(language)('wtd'), reply_markup=choice_keyboard)


def register_handlers_screen_with_filters(dp: Dispatcher):
    dp.register_callback_query_handler(get_screen, Text(equals='getScreen'), state=GetInfo.set_filters)
