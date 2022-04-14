import dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from mstr_connect import get_connection
from database.user_database import DB


class GetInfo(StatesGroup):
    set_language = State()
    find_file = State()
    get_screen = State()
    set_filters = State()
    final = State()


dotenv.load_dotenv('keys.env')
token = os.environ.get('API_KEY')
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
conn = get_connection()
db = DB('database/bot_database.sqlite')

