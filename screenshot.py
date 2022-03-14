from pyppeteer import launch
import asyncio
import logging
#http://dashboards.corp.mvideo.ru/MicroStrategy/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=520F150011EB25866E6D0080EF154E9B&currentViewMedia=1&visMode=0&Server=MSTR-IS01.CORP.MVIDEO.RU&Project=%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0&Port=0&share=1&uid=administrator&pwd=Ceo143566!@
#LP 520F150011EB25866E6D0080EF154E9B
#log 84293CF411EB296FDA820080EFF566F0
#gfk 4E44AA6711EB13AC585C0080EFA5DBEF
#sales 52969EFC11EA3C7B42930080EF857558
#obs 0105984311EA440357CD0080EF354C4B



#https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=520F150011EB25866E6D0080EF154E9B&currentViewMedia=1&visMode=0&Server=10.191.2.88&P

async def get_screen():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://github.com/pyppeteer/pyppeteer')
    await page.screenshot({'path': 'screen.png'})
    await browser.close()





async def screenshot(options = dict()):

    # headless режим
    # ignoreHTTPSErrors игнорить ошибки браузера (н-р сертификат)
    # defaultViewport размер окна
    # timeout_long
    # timeout_short
    # path_screenshot
    # docType: document, report, dossier
    # docID ID документа
    # evt событие (можно посмотреть MicroStrategy\WEB-INF\xml\config\events)
    # path : путь как в браузере
    # Server
    # Project
    # login
    # password
    evt_temp = '2048001' if options.get('docType', 'document') == 'document' else ( '4001' if options.get('docType', 'document') == 'report' else ('3140' if options.get('docType', 'document') == 'dossier' else 'error'))
    evt = options.get('evt', evt_temp)
    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)

    path=options.get('path', 'http://dashboards.corp.mvideo.ru/MicroStrategy/servlet/mstrWeb')
    path+='?evt=' + evt + '&src=mstrWeb.' + options.get('evt', '2048001')
    path+='&' + ( 'document' if options.get('docType', 'document') == 'dossier' else options.get('docType', 'document')) + 'ID=' + options.get('docID', '520F150011EB25866E6D0080EF154E9B') + '&currentViewMedia=1&visMode=0&'
    path+= 'Server=' + options.get('Server','MSTR-IS01.CORP.MVIDEO.RU') + '&'
    path+= 'Project=' + options.get('Project', '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0') + '&Port=0&share=1&'
    path+= 'uid=' + options.get('login', 'administrator') + '&' + 'pwd=' + options.get('password', 'Ceo143566!@')
    path+='&hiddensections=path,dockTop,dockLeft,footer'
    print (path)

    browser = await launch({'headless': options.get('headless', True), 'ignoreHTTPSErrors': options.get('ignoreHTTPSErrors', True), 'defaultViewport': options.get('defaultViewport', {'width': 1920, 'height': 1080})})
    page = await browser.newPage()
    await page.goto(path, {'timeout':timeout_long})

    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType', 'document') == 'document') or (options.get('docType', 'document') == 'dossier') else ( '#UniqueReportID' if options.get('docType', 'document') == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType', 'document') == 'document') or (options.get('docType', 'document') == 'dossier') else ( '#divWaitBox' if options.get('docType', 'document') == 'report' else 'ERROR')


    try:
        await page.waitForSelector(selector_1, {'timeout':timeout_long, 'visible': True} ) #ждем ухода самой загрузки документа и появления загрузки данных борда
        await page.waitForSelector(selector_2, {'timeout':timeout_long, 'hidden': True} ) # ждем пока пропадет окно загрузки данных
        for i in range(5): # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
            try :
                await page.waitForSelector(selector_2, {'timeout':timeout_short, 'visible': True} )
            except:
                await page.screenshot({'path': options.get('path_screenshot', 'example.png')})
                break
            await page.waitForSelector(selector_2, {'timeout':timeout_long, 'hidden': True} )
    except Exception as e:
        logging.exception(e)
        print('error')

    await browser.close()

