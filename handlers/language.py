
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from translate import _

from create_bot_and_conn import GetInfo, bot


# Запоминаем язык, выбранный пользователем
async def change_language(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    language = call.data.split(':')[1]
    async with state.proxy() as data:
        data['language'] = language
        await bot.send_message(call.message.chat.id, text=_(language)('begin'))
    await state.reset_state(with_data=False)


def register_handlers_language(dp: Dispatcher):
    dp.register_callback_query_handler(change_language, Text(startswith='lang:'), state=GetInfo.set_language)
