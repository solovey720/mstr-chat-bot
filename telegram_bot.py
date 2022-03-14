import random

import aiogram as aio
from pyppeteer import launch
import screenshot

#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'0105984311EA440357CD0080EF354C4B','docType': 'document','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))
#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'743FFE22314887C8F2407C9B559ECB4C','docType': 'dossier','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))


token = '5181481316:AAFrV0UNkG7to7AWhwFjFyviQbqHPHH1MtU'
bot = aio.Bot(token)
dp = aio.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введи ID отчета:')


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


async def get_screen():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://github.com/pyppeteer/pyppeteer')
    await page.screenshot({'path': 'screen.png'})
    await browser.close()

aio.executor.start_polling(dp)