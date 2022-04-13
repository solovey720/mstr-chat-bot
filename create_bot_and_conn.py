import dotenv
import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from mstr_connect import get_connection


class GetInfo(StatesGroup):
    set_language = State()
    find_file = State()
    get_screen = State()
    set_filters = State()
    final = State()


dotenv.load_dotenv('keys.env')
token = os.environ.get('API_KEY')
server_link = os.environ.get('SERVER_LINK')
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
#conn = get_connection()
