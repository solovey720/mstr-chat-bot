from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from mstr_connect import get_connection

from database.user_database import DB, sqlite3

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
db = DB('database/bot_database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

# Параметры сервера MSTR
SERVER_LINK = os.environ.get('SERVER_LINK')
SERVER = os.environ.get('SERVER')
PROJECT = os.environ.get('PROJECT')
LOGIN = os.environ.get('LOGIN')
PASSWORD = os.environ.get('PASSWORD')

#Отправлять ли отчеты без секьюрности 
HARD_SECURITY_MODE = False
# Максимально разрешенное количество одновременно запущеных процессов по отправке скриншота для бота 
RUN_LIMIT_BOT = 5
# Максимально разрешенное количество одновременно запущеных процессов по отправке скриншота для подписок
RUN_LIMIT_SCHEDULER = 5
#количество выводимых значений селектора
COUNT_VALUES = 6
# запускать ли окна в хедлес режиме
HEADLESS_MODE = True
# Сколько раз проверять страницу на загруженные данные
COUNT_CHECK_PAGE_LOAD = 4
# Количество секунд на проверку 1 страницы
MAX_TIME_CHECK_PAGE_LOAD = 80
# закрывать ли доступ пользователям не из базы данных
AUTO_CREATE_NEW_USER = True
# закрывать ли доступ пользователям не из базы данных
TRIGGER_CHECKER_TIMEOUT = 1