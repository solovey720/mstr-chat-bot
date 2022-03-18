import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from mstrio.types import ObjectTypes, ObjectSubTypes
import mstr_connect
import aiogram as aio
from pyppeteer import launch
import screenshot
from aiogram.dispatcher.filters.state import StatesGroup, State

#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'0105984311EA440357CD0080EF354C4B','docType': 'document','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))
#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'743FFE22314887C8F2407C9B559ECB4C','docType': 'dossier','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))


token = '5181481316:AAFrV0UNkG7to7AWhwFjFyviQbqHPHH1MtU'
bot = aio.Bot(token)
dp = aio.Dispatcher(bot, storage=MemoryStorage())
conn = mstr_connect.get_connection()

class get_info(StatesGroup):
    find_name = State()



@dp.message_handler(commands=['start'])
async def start_message(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введите /search для поиска отчета')


@dp.message_handler(commands=['search'])
async def start_message(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введи имя отчета:')
    await get_info.find_name.set()


@dp.message_handler(state=get_info.find_name)
async def search_report(message: aio.types.Message, state: FSMContext):
    all_reports = InlineKeyboardMarkup()
    all_documents = InlineKeyboardMarkup()
    async with state.proxy() as data:
        data['find_name'] = message.text
    for report in mstr_connect.search_report(conn, message.text):
        if report.subtype == 768:
            all_reports.add(InlineKeyboardButton(report.name, callback_data=f'report_{report.id}'))
    for document in mstr_connect.search_document(conn, message.text):
        all_documents.add(InlineKeyboardButton(document.name, callback_data=f'document_{document.id}'))
    await state.finish()
    await bot.send_message(message.from_user.id, 'Список доступных репортов:', reply_markup=all_reports)
    await bot.send_message(message.from_user.id, 'Список доступных документов:', reply_markup=all_documents)
    print('user_chat_id'+str(message.from_user.id))


@dp.callback_query_handler(Text(startswith=['report_', 'document_']))
async def get_screenshot(call: aio.types.CallbackQuery):
    file_type = call.data.split('_')[0]
    file_id = call.data.split('_')[1]

    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id+1) if file_type == 'report' else await bot.delete_message(call.message.chat.id, call.message.message_id-1)

    await call.answer('Сейчас будет отправлен скриншот отчета',)
    print(file_type)
    print(file_id)

    html = await screenshot.screenshot_html({'docID': file_id, 'docType': file_type})
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile('example.png'))

    yes_no_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data=f'addFilter_{file_type}_{file_id}'),
                                                 InlineKeyboardButton('No', callback_data='NoFilter'))
    await bot.send_message(call.message.chat.id, 'Хотите добавить фильтр на отчет?', reply_markup=yes_no_keyboard)


@dp.callback_query_handler(Text(startswith='documentID_'))
async def get_screenshot(call: aio.types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id-1)

    document_id = call.data.split('_')[1]

    await call.answer('Сейчас будет отправлен скриншот отчета',)
    print(document_id)
    html = await screenshot.screenshot_html({'docID' : document_id, 'docType': 'document'})
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile('example.png'))

    yes_no_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data='addFilter_'+document_id),
                                                 InlineKeyboardButton('No', callback_data='NoFilter'))
    print('user_chat_id' + str(call.message.from_user.id))
    await bot.send_message(call.message.chat.id, 'Хотите добавить фильтр на отчет?', reply_markup=yes_no_keyboard)




@dp.message_handler()
async def send(message: aio.types.Message):
    if len(message.text) != 32:
        await bot.send_message(message.from_user.id, 'Некорректный ID отчета')
    else:
        await bot.send_message(message.from_user.id, 'Делаем скриншот. Может занять некоторое время...')
        count = random.randint(0,100000)
        print(count)
        await screenshot.screenshot({'docID': message.text})
        print(count)
        photo = open('example.png', 'rb')
        await bot.send_photo(message.from_user.id, photo=photo)



aio.executor.start_polling(dp)