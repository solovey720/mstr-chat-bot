import asyncio
from pyppeteer import launch

async def main():
    browser = await launch({'headless': True, 'ignoreHTTPSErrors': True, 'defaultViewport': {'width': 1920, 'height': 1080}})
    page = await browser.newPage()
    await page.goto('http://dashboards.corp.mvideo.ru:80/MicroStrategy/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=520F150011EB25866E6D0080EF154E9B&currentViewMedia=1&visMode=0&Server=MSTR-IS01.CORP.MVIDEO.RU&Project=%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0&Port=0&share=1&uid=administrator&pwd=Ceo143566!@',
    {'waitUntil': 'networkidle0'})
    await page.screenshot({'path': 'test\example.png'})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())