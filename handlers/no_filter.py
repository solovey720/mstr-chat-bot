from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot_and_conn import GetInfo, bot
from aiogram.types import CallbackQuery, User
from translate import _
from screenshot import close_page
from aiogram import Dispatcher


# @dp.callback_query_handler(Text(startswith='noFilter'), state=GetInfo.set_filters)
async def no_filter(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        language = data['language']
        await call.message.delete()
        await bot.send_message(call.message.chat.id, _(language)('type_search'))
    await state.finish()
    await close_page(User.get_current().id)


def register_handlers_no_filters(dp: Dispatcher):
    dp.register_callback_query_handler(no_filter, Text(startswith='noFilter'), state=GetInfo.set_filters)