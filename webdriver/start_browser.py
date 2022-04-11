from pyppeteer import launch
import asyncio

async def on_startup(): 
    #'ignoreDefaultArgs': ['--force-fieldtrials=AutomaticTabDiscarding/Disabled'],
    global browser
    browser = await launch({ 'headless': True, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})

asyncio.get_event_loop().run_until_complete(on_startup())
