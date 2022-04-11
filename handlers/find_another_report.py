from create_bot_and_conn import bot, GetInfo
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, User
from aiogram.dispatcher import FSMContext
from screenshot import close_page
from translate import _
from aiogram import Dispatcher


# @dp.callback_query_handler(Text(equals='findAnother'), state=GetInfo.set_filters)
async def find_another_report(call: CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']
    await close_page(User.get_current().id)
    await state.finish()
    await bot.send_message(call.message.chat.id, _(language)('type_search'))


def register_handlers_find_another_report(dp: Dispatcher):
    dp.register_callback_query_handler(find_another_report, Text(equals='findAnother'), state=GetInfo.set_filters)
