
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, bot

from webdriver.scheduler import get_selectors, get_values

from translate import _


# Выводим список всех селекторов
async def get_all_selectors(call: CallbackQuery, state: FSMContext):
    # TODO: сделать обнуление словарей selectors_multi, selectors_wo_multi
    language = ''
    async with state.proxy() as data:
        language = data['language']
    await call.message.delete()

    selectors_multi, selectors_wo_multi = await get_selectors(User.get_current().id)

    # отправляем селекторы с мультивыбором
    if selectors_multi:
        selectors_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_multi:
            if selector[0] not in ('S', 's'):
                selectors_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:mult:{selector}')
                selectors_multi_keyboard.add(selectors_multi_button)
                async with state.proxy() as data:
                    data['selectors_multi'].update({selector: selectors_multi[selector]})
        await bot.send_message(call.message.chat.id, _(language)('mult_selectors'),
                               reply_markup=selectors_multi_keyboard)

    # отправляем селекторы без мультивыбора
    if selectors_wo_multi:
        selectors_wo_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_wo_multi:
            if selector[0] not in ('S', 's'):
                selectors_wo_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:womult:{selector}')
                selectors_wo_multi_keyboard.add(selectors_wo_multi_button)
                async with state.proxy() as data:
                    data['selectors_wo_multi'].update({selector: selectors_wo_multi[selector]})
        await bot.send_message(call.message.chat.id, _(language)('wo_mult_selectors'),
                               reply_markup=selectors_wo_multi_keyboard)

    send_screen_keyboard = InlineKeyboardMarkup()
    send_screen_button = InlineKeyboardButton(_(language)('get_screen'), callback_data='getScreen')
    send_screen_keyboard.add(send_screen_button)
    await bot.send_message(call.message.chat.id, _(language)('get_screen'), reply_markup=send_screen_keyboard)


# Выводим список всех значений выбранного селектора
async def get_selector_values(call: CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']

    selector_name = call.data.split(':')[2]
    selector_type = call.data.split(':')[1]
    selector_ctl_name = ''
    if selector_type == 'mult':
        async with state.proxy() as data:
            selector_ctl_name = data['selectors_multi'][selector_name] + f';{selector_name}'
    else:
        async with state.proxy() as data:
            selector_ctl_name = data['selectors_wo_multi'][selector_name] + f';{selector_name}'

    # добавляем ctl селектора в словарь filters
    async with state.proxy() as data:
        data['active_selector'] = selector_ctl_name
        data['filters'].update({selector_ctl_name: []})

    selector_values = await get_values(User.get_current().id, selector_ctl_name.split(';')[0])
    async with state.proxy() as data:
        data['selector_values'] = selector_values

    if selector_values:
        selector_values_keyboard = InlineKeyboardMarkup()
        for value in selector_values:
            selector_values_button = InlineKeyboardButton(value, callback_data=f'val:{selector_type}:{value}')
            selector_values_keyboard.add(selector_values_button)

        if selector_type == 'mult':
            await bot.edit_message_text(text=_(language)('sel_val_mult').format(selector_name),
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=selector_values_keyboard)
            try:
                await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
                await bot.delete_message(call.message.chat.id, call.message.message_id + 2)
            except Exception as e:
                await bot.delete_message(call.message.chat.id, call.message.message_id + 2)
        else:
            await bot.edit_message_text(text=_(language)('sel_val_wo_mult').format(selector_name),
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=selector_values_keyboard)

            await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
            async with state.proxy() as data:
                if data['selectors_multi']:
                    await bot.delete_message(call.message.chat.id, call.message.message_id - 1)

        choice_keyboard = InlineKeyboardMarkup()
        choose_selector_button = InlineKeyboardButton(_(language)('more_selectors'), callback_data='yesFilter')
        choose_screen_button = InlineKeyboardButton(_(language)('get_screen'), callback_data='getScreen')
        choice_keyboard.add(choose_selector_button, choose_screen_button)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=_(language)('set_sel_val'),
                               reply_markup=choice_keyboard)


# Запоминаем выбранное значение(-я) у селектора
async def set_selector_value(call: CallbackQuery, state: FSMContext):
    language = ''
    async with state.proxy() as data:
        language = data['language']

    selector_type = call.data.split(':')[1]
    selector_value_name = call.data.split(':')[2]
    selected_values = []

    async with state.proxy() as data:
        selector_value = data['selector_values'][selector_value_name]
        selector_ctl = data['active_selector']
        if selector_type == 'mult':
            data['filters'][selector_ctl].append({selector_value: selector_value_name})
        else:
            data['filters'][selector_ctl] = [{selector_value: selector_value_name}]
        for value_name in data['filters'][selector_ctl]:
            selected_values.append(list(value_name.values())[0])

        choice_keyboard = InlineKeyboardMarkup()
        choose_selector_button = InlineKeyboardButton(_(language)('more_selectors'), callback_data='yesFilter')
        choose_screen_button = InlineKeyboardButton(_(language)('get_screen'), callback_data='getScreen')
        choice_keyboard.add(choose_selector_button, choose_screen_button)

        await bot.send_message(chat_id=call.message.chat.id, text=_(language)('selector_set').format(selected_values))


def register_handlers_set_selectors(dp: Dispatcher):
    dp.register_callback_query_handler(get_all_selectors, Text(startswith='yesFilter'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(get_selector_values, Text(startswith='sel:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(set_selector_value, Text(startswith='val:'), state=GetInfo.set_filters)
