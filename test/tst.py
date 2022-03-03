import asyncio
from pyppeteer import launch
#LP 520F150011EB25866E6D0080EF154E9B
#log 84293CF411EB296FDA820080EFF566F0
#gfk 4E44AA6711EB13AC585C0080EFA5DBEF
#sales 52969EFC11EA3C7B42930080EF857558
#obs 0105984311EA440357CD0080EF354C4B
docID = '0105984311EA440357CD0080EF354C4B'

async def main():
    browser = await launch({'headless': True, 'ignoreHTTPSErrors': True, 'defaultViewport': {'width': 1920, 'height': 1080}})
    page = await browser.newPage()
    await page.goto('http://dashboards.corp.mvideo.ru:80/MicroStrategy/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID='+ docID +'&currentViewMedia=1&visMode=0&Server=MSTR-IS01.CORP.MVIDEO.RU&Project=%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0&Port=0&share=1&uid=administrator&pwd=Ceo143566!@')

    try :
        await page.waitForSelector('#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal', {'timeout':60000, 'visible': True} )
        await page.waitForSelector('#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal', {'timeout':60000, 'hidden': True} )
        await page.waitForSelector('#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal', {'timeout':10000, 'visible': True} )
    except:
        await page.screenshot({'path': 'git/mstr-chat-bot/test/example.png'})
    
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())