
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from mstr_connect import get_connection

from database.user_database import DB

import dotenv

import os


# Класс для машины состояний
class GetInfo(StatesGroup):
    set_language = State()
    find_file = State()
    get_screen = State()
    set_filters = State()
    final = State()


dotenv.load_dotenv('keys.env')

# Инициализируем бота и подключение к MSTR
token = os.environ.get('API_KEY')
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
conn = get_connection()

# Подключаем базу данных
db = DB('database/bot_database.sqlite')

# Параметры сервера MSTR
SERVER_LINK = os.environ.get('SERVER_LINK')
SERVER = os.environ.get('SERVER')
PROJECT = os.environ.get('PROJECT')
LOGIN = os.environ.get('LOGIN')
PASSWORD = os.environ.get('PASSWORD')

#TODO: установить дефолтное значение language
