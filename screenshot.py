from matplotlib.style import use
from pyppeteer import launch
import asyncio
import logging
import dotenv
import os

global browser
dotenv.load_dotenv('keys.env')
"""
asyncio.get_event_loop().run_until_complete(create_page(1,{'docID': 'EA706ACB43C4530927380DB3B07E0889'}) )

#asyncio.get_event_loop().run_until_complete(get_filter_screen(1))
asyncio.get_event_loop().run_until_complete(create_page(2,{'docID': '8CD564B54D2ED4AFD358F3853610D647'}) )
asyncio.get_event_loop().run_until_complete(get_filter_screen(2))
#asyncio.get_event_loop().run_until_complete(get_filter_screen(1))
asyncio.get_event_loop().run_until_complete(get_filter_screen(1, {'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'], 'filters': {'IGK719A420311EA16852B700080EF55FCB9':['h1;264614C648E9C743C4283B8137C8D9BA','h10;264614C648E9C743C4283B8137C8D9BA']}}))
#asyncio.get_event_loop().run_until_complete(get_filter_screen(2))
"""

async def create_page(user_id, options=dict()):
    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)
    path = options.get('path', os.environ.get('SERVER')+'/MicroStrategy/servlet/mstrWeb')
    docID = options.get('docID', 'C4DB9BA7BF457B5B6D345090FF2BA99F')
    docType = options.get('docType', 'document')
    # TODO: как назвать server, если server двумя строчками выше?
    server = options.get('Server', 'DESKTOP-2RSMLJR') #КАК НАЗВАТЬ???????????????????????
    project = options.get('Project', os.environ.get('PROJECT'))
    login = options.get('login', os.environ.get('LOGIN'))
    password = options.get('password', os.environ.get('PASSWORD'))
    screen_width = 1920
    screen_height = 1080

    evt_temp = '2048001' if docType == 'document' else (
        '4001' if docType == 'report' else (
            '3140' if docType == 'dossier' else 'error'))
    evt = options.get('evt', evt_temp)

    path += '?evt=' + evt + '&src=mstrWeb.' + evt
    path += '&' + ('document' if docType == 'dossier' else docType) + 'ID=' + docID + '&currentViewMedia=1&visMode=0&'
    path += 'Server=' + server + '&'
    path += 'Project=' + project + '&Port=0&share=1&'
    path += 'uid=' + login + '&' + 'pwd=' + password
    path += '&hiddensections=path,dockTop,dockLeft,footer'

    page = await browser.newPage()
    page.user_id = user_id

    await page.goto(path, {'timeout': timeout_long})

    ############################ press 'continue'
    await page.waitForSelector('#\\33 054', {'timeout': timeout_long, 'visible': True})
    await page.click('#\\33 054')
    ############################

    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (
                docType == 'dossier') else (
        '#UniqueReportID' if docType == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (
                docType == 'dossier') else (
        '#divWaitBox' if docType == 'report' else 'ERROR')

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
                return
            await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})
    except Exception as e:
        logging.exception(e)
        print('error')


async def get_filter_screen(user_id, options=dict()):
    page = await get_page_by_id(user_id)

    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)
    docType = options.get('docType', 'document')
    screen_name = options.get('path_screenshot', f'{user_id}.png')

    security_sel = 'S_security'
    security_val = options.get('security', [])

    filters_sel = options.get('filters', {})

    if not (security_val or filters_sel):
        await page.screenshot({'path': screen_name})
        return

    if security_val:
        ctlkey = (await get_selectors(user_id))[security_sel]
        tmp = await get_values(user_id, ctlkey)
        security_ctl_val = []
        for i in security_val:
            security_ctl_val.append(tmp[i])
        await request_set_selector(user_id, {'ctlKey': f'{ctlkey}', 'elemList': list_to_str(security_ctl_val)})

    if filters_sel:
        for i in filters_sel.keys():
            print(i)
            await request_set_selector(user_id, {'ctlKey': i, 'elemList': list_to_str(filters_sel[i])})

    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (
                docType == 'dossier') else (
        '#UniqueReportID' if docType == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (
                docType == 'dossier') else (
        '#divWaitBox' if docType == 'report' else 'ERROR')

    await apply_selectors(user_id)

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
                await page.screenshot({'path': screen_name})
                return
            await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})
    except Exception as e:
        logging.exception(e)
        print('error')

    return


async def get_selectors(user_id):
    page = await get_page_by_id(user_id)
    HTML = await page.evaluate('document.body.innerHTML')
    select_multi = dict()
    select_wo_multi = dict()
    find_111 = HTML.find('\"t\":111') + 1
    while find_111 != 0:
        HTML = HTML[find_111:]
        HTML = HTML[HTML.find('\"n\":\"') + 5:]
        name = HTML[:HTML.find('\"')]
        HTML = HTML[HTML.find('\"ckey\":\"') + 8:]
        ckey = HTML[:HTML.find('\"')]

        HTML = HTML[HTML.find('\"multi\":') + 8:]
        if HTML[0] == 't':
            select_multi[name] = ckey
        else:
            select_wo_multi[name] = ckey
        find_111 = HTML.find('\"t\":111') + 1
    return select_multi, select_wo_multi


async def get_values(user_id, ckey):
    page = await get_page_by_id(user_id)
    HTML = await page.evaluate('document.body.innerHTML')
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


async def request_set_selector(user_id, options=dict()):
    page = await get_page_by_id(user_id)
    url = options.get('url', os.environ.get('SERVER')+'/MicroStrategy/servlet/taskProc')
    ctlKey = options.get('ctlKey', 'W5121A375615A451CA272FD10697EA8EA')
    elemList = options.get('elemList', 'h29;77ECA0D9445F155A4B08DFAC49FC9624')

    taskid = options.get('taskid', 'mojoRWManipulation')
    rwb = await page.evaluate('mstrApp.docModel.bs')
    messageID = await page.evaluate('mstrApp.docModel.mid')
    mstr_now = await page.evaluate('mstrmojo.now()')
    servlet = await page.evaluate('mstrApp.servletState')
    keyContext = await page.evaluate(f'mstrApp.docModel.getNodeDataByKey("{ctlKey}").defn.ck')

    await page.evaluate(f'''
    url = \'{url}\'
    fetch(url, {{
    method: 'POST',
        headers: {{
        'Content-type': 'application/x-www-form-urlencoded',
        }},
    body:"taskId={taskid}&rwb={rwb}&messageID={messageID}&stateID=-1&params=%7B%22actions%22%3A%5B%7B%22act%22%3A%22setSelectorElements%22%2C%22keyContext%22%3A%22{keyContext}%22%2C%22ctlKey%22%3A%22{ctlKey}%22%2C%22elemList%22%3A%22{elemList}%22%2C%22isVisualization%22%3Afalse%2C%22include%22%3Atrue%2C%22tks%22%3A%22W12390BF5EDEF41D8A507193CEF784240%22%7D%5D%2C%22partialUpdate%22%3A%7B%22selectors%22%3A%5B%22W5121A375615A451CA272FD10697EA8EA%22%5D%7D%2C%22style%22%3A%7B%22params%22%3A%7B%22treesToRender%22%3A3%7D%2C%22name%22%3A%22RWDocumentMojoStyle%22%7D%7D&zoomFactor=1&styleName=RWDocumentMojoStyle&taskContentType=json&taskEnv=xhr&xts={mstr_now}&mstrWeb={servlet}"
    }})   
    ''')

# зачем выносить это в отдельную функцию?
async def apply_selectors(user_id):
    page = await get_page_by_id(user_id)
    await page.evaluate('mstrApp.docModel.controller.refresh()')



async def on_startup(_):
    global browser
    browser = await launch({'headless': True, 'ignoreHTTPSErrors': True, 'autoClose': False,
                            'defaultViewport': {'width': 1920, 'height': 1080}})


async def get_page_by_id(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            return i


async def close_page(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            i.close()


def list_to_str(val: list) -> str:
    str = val.pop()
    str = ''
    for i in val:
        str += '\\u001e' + i
    return str