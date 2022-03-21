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
async def screenshot(options = dict()):
    timeout_long = 60000
    timeout_short = 3000
    path = 'https://dashboard-temp/MicroStrategy/servlet/mstrWeb'
    docID = 'C4DB9BA7BF457B5B6D345090FF2BA99F'
    docType = 'document'
    server = '10.191.2.88'
    project = 'Дашборды+оперсовета'
    login = 'administrator'
    password = 'Ceo143566'
    screen_width = 1920
    screen_height = 1080
    screen_name = 'test.png'

    evt_temp = '2048001' if options.get('docType', docType) == 'document' else ('4001' if options.get('docType', docType) == 'report' else ('3140' if options.get('docType', docType) == 'dossier' else 'error'))
    evt = options.get('evt', evt_temp)
    timeout_long = options.get('timeout_long', timeout_long)
    timeout_short = options.get('timeout_short', timeout_short)

    path=options.get('path', path)
    path+='?evt=' + evt + '&src=mstrWeb.' + options.get('evt', '2048001')
    path+='&' + ('document' if options.get('docType', docType) == 'dossier' else options.get('docType', docType)) + 'ID=' + options.get('docID', docID) + '&currentViewMedia=1&visMode=0&'
    path+= 'Server=' + options.get('Server', server) + '&'
    path+= 'Project=' + options.get('Project', project) + '&Port=0&share=1&'
    path+= 'uid=' + options.get('login', login) + '&' + 'pwd=' + options.get('password', password)
    path+='&hiddensections=path,dockTop,dockLeft,footer'
    print (path)

    browser = await launch({'headless': options.get('headless', False), 'ignoreHTTPSErrors': options.get('ignoreHTTPSErrors', True), 'defaultViewport': options.get('defaultViewport', {'width': screen_width, 'height': screen_height})})
    page = await browser.newPage()
    await page.goto(path, {'timeout':timeout_long})

    # нажимаем на 'continue
    #await page.waitForSelector('#\\33 054', {'timeout': timeout_long,'visible': True})
    #await page.click('#\\33 054')

    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType', 'document') == 'document') or (options.get('docType', 'document') == 'dossier') else ( '#UniqueReportID' if options.get('docType', 'document') == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType', 'document') == 'document') or (options.get('docType', 'document') == 'dossier') else ( '#divWaitBox' if options.get('docType', 'document') == 'report' else 'ERROR')
    try:
        await page.waitForSelector(selector_1, {'timeout':timeout_long, 'visible': True} ) #ждем ухода самой загрузки документа и появления загрузки данных борда
        await page.waitForSelector(selector_2, {'timeout':timeout_long, 'hidden': True} ) # ждем пока пропадет окно загрузки данных
        for i in range(5): # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
            try :
                await page.waitForSelector(selector_2, {'timeout':timeout_short, 'visible': True} )
            except:
                await page.screenshot({'path': options.get('path_screenshot', screen_name)})
                break
            await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})
    except Exception as e:
        logging.exception(e)
        print('error')

    await browser.close()


async def screenshot_html(options=dict(), selectors=''):
    timeout_long = 60000
    timeout_short = 3000
    path = 'https://d1bd-213-135-80-34.ngrok.io/MicroStrategy/servlet/mstrWeb'
    docID = 'C4DB9BA7BF457B5B6D345090FF2BA99F'
    docType = 'document'
    server = 'DESKTOP-2RSMLJR'
    project = 'New+Project'
    login = 'administrator'
    password = ''
    screen_width = 1920
    screen_height = 1080
    screen_name = 'test.png'

    evt_temp = '2048001' if options.get('docType', docType) == 'document' else (
        '4001' if options.get('docType', docType) == 'report' else (
            '3140' if options.get('docType', docType) == 'dossier' else 'error'))
    evt = options.get('evt', evt_temp)
    timeout_long = options.get('timeout_long', timeout_long)
    timeout_short = options.get('timeout_short', timeout_short)

    path = options.get('path', path)
    path += '?evt=' + evt + '&src=mstrWeb.' + evt
    path += '&' + ('document' if options.get('docType', docType) == 'dossier' else options.get('docType', docType)) + 'ID=' + options.get(
        'docID', docID) + '&currentViewMedia=1&visMode=0&'
    path += 'Server=' + options.get('Server', server) + '&'
    path += 'Project=' + options.get('Project',
                                     project) + '&Port=0&share=1&'
    path += 'uid=' + options.get('login', login) + '&' + 'pwd=' + options.get('password', password)
    path += '&hiddensections=path,dockTop,dockLeft,footer'

    path += selectors
    ##############
    #path += '&evt=' + '1024001' + '&src=mstrWeb.' + 'oivm.rwb.1024001'
    #path += '&events=-2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.WC5D6239510A84DC09D38527793A12086*.elemList*.h1;264614C648E9C743C4283B8137C8D9BA*.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0.2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.W5121A375615A451CA272FD10697EA8EA*.elemList*.h1;77ECA0D9445F155A4B08DFAC49FC9624*.elemList*.h23;77ECA0D9445F155A4B08DFAC49FC9624*.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0.2048014*.mstrWeb***.oivm***.rwb***.2048014_'
    #path += '&evtorder=2048001%2c1024001&2048001=1&1024001=1'
    ##############
    print(path)
    ####################################################
    browser = await launch(
        {'headless': options.get('headless', False), 'ignoreHTTPSErrors': options.get('ignoreHTTPSErrors', True),
         'defaultViewport': options.get('defaultViewport', {'width': screen_width, 'height': screen_height})})
    page = await browser.newPage()
    await page.goto(path, {'timeout': timeout_long})

    ############################ press 'continue'
    await page.waitForSelector('#\\33 054', {'timeout': timeout_long,'visible': True})
    await page.click('#\\33 054')
    ############################
    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType', docType) == 'document') or (options.get('docType', docType) == 'dossier') else (
        '#UniqueReportID' if options.get('docType', 'document') == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType',
                                                                                    docType) == 'document') or (
                                                                                   options.get('docType', docType) == 'dossier') else (
        '#divWaitBox' if options.get('docType', docType) == 'report' else 'ERROR')

    try:
        await page.waitForSelector(selector_1, {'timeout': timeout_long,
                                                'visible': True})  # ждем ухода самой загрузки документа и появления загрузки данных борда
        await page.waitForSelector(selector_2,
                                   {'timeout': timeout_long, 'hidden': True})  # ждем пока пропадет окно загрузки данных
        for i in range(
                5):  # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
            try:
                await page.waitForSelector(selector_2, {'timeout': timeout_short, 'visible': True})

            except:
                await page.screenshot({'path': options.get('path_screenshot', screen_name)})
                HTML = await page.evaluate('document.body.innerHTML')
                break
            await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})
    except Exception as e:
        logging.exception(e)
        print('error')

    # selectors = get_selectors(HTML)
    # tst= get_values(HTML, selectors['Актер'])
    # print(tst)

    await browser.close()
    return HTML


def get_selectors(HTML):
    select = dict()
    find_111 = HTML.find('\"t\":111') + 1
    while find_111 != 0:
        HTML = HTML[find_111:]
        HTML = HTML[HTML.find('\"n\":\"') + 5:]
        name = HTML[:HTML.find('\"')]
        HTML = HTML[HTML.find('\"ckey\":\"') + 8:]
        ckey = HTML[:HTML.find('\"')]
        select[name[0:6]] = ckey
        find_111 = HTML.find('\"t\":111') + 1
    return select


def get_values(HTML, ckey):
    val = dict()
    HTML = HTML[HTML.find('\"k\":\"' + ckey + '\"'):]
    begin = HTML.find('\"elms\":[') + 9
    end = HTML[begin:].find(']') - 1
    values = HTML[begin:begin + end].split('},{')
    for i in values:
        tmp = i
        tmp = tmp[tmp.find('\"v\":\"') + 5:]
        value = tmp[:tmp.find('\"')]
        tmp = tmp[tmp.find('\"n\":\"') + 5:]
        name = tmp[:tmp.find('\"')]
        val[name] = value
    return val


def get_path(options=dict()):
    timeout_long = 60000
    timeout_short = 3000
    path = 'https://dashboard-temp/MicroStrategy/servlet/mstrWeb'
    docID = 'C4DB9BA7BF457B5B6D345090FF2BA99F'
    docType = 'document'
    server = '10.191.2.88'
    project = 'Дашборды+оперсовета'
    login = 'administrator'
    password = 'Ceo143566'
    screen_width = 1920
    screen_height = 1080
    screen_name = 'test.png'

    evt_temp = '2048001' if options.get('docType', docType) == 'document' else (
        '4001' if options.get('docType', docType) == 'report' else (
            '3140' if options.get('docType', docType) == 'dossier' else 'error'))
    evt = options.get('evt', evt_temp)
    timeout_long = options.get('timeout_long', timeout_long)
    timeout_short = options.get('timeout_short', timeout_short)

    path = options.get('path', path)
    path += '?evt=' + evt + '&src=mstrWeb.' + evt
    path += '&' + ('document' if options.get('docType', docType) == 'dossier' else options.get('docType', docType)) + 'ID=' + options.get(
        'docID', docID) + '&currentViewMedia=1&visMode=0&'
    path += 'Server=' + options.get('Server', server) + '&'
    path += 'Project=' + options.get('Project',
                                     project) + '&Port=0&share=1&'
    path += 'uid=' + options.get('login', login) + '&' + 'pwd=' + options.get('password', password)
    path += '&hiddensections=path,dockTop,dockLeft,footer'
    ##############
    #path += '&evt=' + '1024001' + '&src=mstrWeb.' + 'oivm.rwb.1024001'
    #path += '&events=-2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.WC5D6239510A84DC09D38527793A12086*.elemList*.h1;264614C648E9C743C4283B8137C8D9BA*.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0.2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.W5121A375615A451CA272FD10697EA8EA*.elemList*.h1;77ECA0D9445F155A4B08DFAC49FC9624*.elemList*.h23;77ECA0D9445F155A4B08DFAC49FC9624*.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0.2048014*.mstrWeb***.oivm***.rwb***.2048014_'
    #path += '&evtorder=2048001%2c1024001&2048001=1&1024001=1'
    ##############
    print(path)


async def get_screen(path, options=dict()):
    print(path)
    browser = await launch({'headless': options.get('headless', False),
                            'ignoreHTTPSErrors': options.get('ignoreHTTPSErrors', True),
                            'defaultViewport': options.get('defaultViewport', {'width': options.get('screen_width', 1920), 'height': options.get('screen_height', 1080)})
                            })
    page = await browser.newPage()
    await page.goto(path, {'timeout': options.get('timeout_long', 60000)})

    ############################ press 'continue'
    #await page.waitForSelector('#\\33 054', {'timeout': timeout_long,'visible': True})
    #await page.click('#\\33 054')
    ############################

    if (options.get('docType') == 'document') or (options.get('docType') == 'dossier'):
        selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal'
        selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal'
    elif options.get('docType') == 'report':
        selector_1 = '#UniqueReportID'
        selector_2 = '#divWaitBox'
    else:
        selector_1 = 'ERROR'
        selector_2 = 'ERROR'

    try:
        await page.waitForSelector(selector_1, {'timeout': options.get('timeout_long', 60000), 'visible': True})  # ждем ухода самой загрузки документа и появления загрузки данных борда
        await page.waitForSelector(selector_2, {'timeout': options.get('timeout_long', 60000), 'hidden': True})  # ждем пока пропадет окно загрузки данных
        for i in range(5):  # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
            try:
                await page.waitForSelector(selector_2, {'timeout': options.get('timeout_short', 3000), 'visible': True})

            except:
                await page.screenshot({'path': options.get('path_screenshot', 'example.png')})
                break
            await page.waitForSelector(selector_2, {'timeout': options.get('timeout_long', 60000), 'hidden': True})
    except Exception as e:
        logging.exception(e)
        print('errorrrrrrrr')

    await browser.close()