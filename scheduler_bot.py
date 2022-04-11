import random
from scheduler import scheduler, get_user_jobs
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
#from scheduler import scheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from mstrio.types import ObjectTypes, ObjectSubTypes
import mstr_connect

from pyppeteer import launch
import screenshot
from aiogram.dispatcher.filters.state import StatesGroup, State
from init_bot import bot, dp
import json
from translate import _
import dotenv
import os
import aiogram as aio

dotenv.load_dotenv('keys.env')



scheduler.remove_all_jobs()
@dp.message_handler(commands=['sched'], state=None)
async def start_command(message: aio.types.Message):
    print('s')
    
    user_id = aio.types.User.get_current().id
    scheduler.add_job(send_sched_photo,  "interval", seconds=20, replace_existing=True, args=[1, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr', name='sec_withsec_withfiltr')
    scheduler.add_job(send_sched_photo,  "interval", seconds=15, replace_existing=True, args=[2, { 'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withfiltr', name='sec_withfiltr')
    scheduler.add_job(send_sched_photo,  "interval", seconds=10, replace_existing=True, args=[3, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER']}],id=f'{user_id}_sec_withsec', name='sec_withsec')
    scheduler.add_job(send_sched_photo,  "interval", seconds=5, replace_existing=True, args=[4],id=f'{user_id}_sec', name='sec')
    print(get_user_jobs(str(user_id)))
    print('f')
    #scheduler.add_job(screenshot.create_page,  "interval", seconds=3, replace_existing=True, args=[aio.types.User.get_current().id,{'docID': 'EA706ACB43C4530927380DB3B07E0889'}],id='2')
    #print('sched')
    #await screenshot.create_page(aio.types.User.get_current().id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'})
    #await screenshot.get_filter_screen(aio.types.User.get_current().id)
    #await bot.send_photo(chat_id=aio.types.User.get_current().id, photo=InputFile(str(aio.types.User.get_current().id) + '.png'))

async def send_sched_photo(user_id: int, options=dict()): 
    await screenshot.scheduler_dashboard(user_id, options)
    #await bot.send_photo(chat_id=user_id, photo=InputFile(str((-1) * user_id) + '.png'))
    #os.remove(str((-1) * user_id) + '.png')


