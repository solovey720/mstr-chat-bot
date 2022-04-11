import os
from pyppeteer import launch
from aiogram.types import InputFile
import asyncio
import logging
#http://dashboards.corp.mvideo.ru/MicroStrategy/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=520F150011EB25866E6D0080EF154E9B&currentViewMedia=1&visMode=0&Server=MSTR-IS01.CORP.MVIDEO.RU&Project=%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0&Port=0&share=1&uid=administrator&pwd=Ceo143566!@
#LP 520F150011EB25866E6D0080EF154E9B
#log 84293CF411EB296FDA820080EFF566F0
#gfk 4E44AA6711EB13AC585C0080EFA5DBEF
#sales 52969EFC11EA3C7B42930080EF857558
#obs 0105984311EA440357CD0080EF354C4B





async def create_page(user_id, options=dict(), new_browser = None):

    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)
    path = options.get('path', 'http://41b7-213-135-80-34.ngrok.io/MicroStrategy/servlet/mstrWeb') # https://dashboard-temp/MicroStrategy/servlet/mstrWeb
    docID = options.get('docID', 'C4DB9BA7BF457B5B6D345090FF2BA99F')
    docType = options.get('docType', 'document')
    server = options.get('Server', 'DESKTOP-2RSMLJR')
    project = options.get('Project', 'New+Project')
    login = options.get('login', 'administrator')
    password = options.get('password', '')

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

    if not new_browser:
        #global browser
        page = await browser.newPage()
    else: 
        page = await new_browser.newPage()

    page.user_id = user_id

    await page.goto(path, {'timeout': timeout_long})
    #await create_audio (user_id)
    ############################ press 'continue'
    await page.waitForSelector('#\\33 054', {'timeout': timeout_long,'visible': True})
    await page.click('#\\33 054')
    #await create_audio (user_id)
    ############################
    
    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (docType == 'dossier') else (
        '#UniqueReportID' if docType == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (docType == 'dossier') else (
        '#divWaitBox' if docType == 'report' else 'ERROR')

    try:
        await page.waitForSelector(selector_1, {'timeout': timeout_long, 'visible': True})  # ждем ухода самой загрузки документа и появления загрузки данных борда
        await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})  # ждем пока пропадет окно загрузки данных
        for i in range(5):  # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
            try:
                await page.waitForSelector(selector_2, {'timeout': timeout_short, 'visible': True})
            except:
                return
            await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})
    except Exception as e:
        logging.exception(e)
        print('error')
    


async def get_filter_screen(user_id, options=dict(), new_browser = None):
    if not new_browser:
        page = await get_page_by_id(user_id)
    else: 
        page = (await new_browser.pages())[1]
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
        a, b = await get_selectors(user_id, new_browser=new_browser)
        all_selectors = a | b
        ctlkey = (all_selectors)[security_sel]
        tmp = await get_values(user_id, ctlkey, new_browser=new_browser)
        security_ctl_val=[]
        for i in security_val:
            security_ctl_val.append(tmp[i])
        await request_set_selector(user_id, {'ctlKey': f'{ctlkey}', 'elemList': list_to_str(security_ctl_val)}, new_browser=new_browser)
    
    if filters_sel: 
        for i in filters_sel.keys():
            await request_set_selector(user_id, {'ctlKey': i, 'elemList': list_to_str(filters_sel[i])}, new_browser=new_browser)
    
    
    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (docType == 'dossier') else (
        '#UniqueReportID' if docType == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (docType == 'dossier') else (
        '#divWaitBox' if docType == 'report' else 'ERROR')
    
    await apply_selectors(user_id, new_browser=new_browser)
 
    try:
        await page.waitForSelector(selector_1, {'timeout': timeout_long, 'visible': True})  # ждем ухода самой загрузки документа и появления загрузки данных борда
        await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})  # ждем пока пропадет окно загрузки данных
        for i in range(5):  # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
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


async def get_selectors(user_id, new_browser = None):
    if not new_browser:
        page = await get_page_by_id(user_id)
    else: 
        page = (await new_browser.pages())[1]
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
        if HTML[0]=='t':
            select_multi[name] = ckey
        else:
            select_wo_multi[name] = ckey
        find_111 = HTML.find('\"t\":111') + 1
    return select_multi, select_wo_multi 


async def get_values(user_id, ckey, new_browser = None):
    
    if not new_browser:
        page = await get_page_by_id(user_id)
    else: 
        page = (await new_browser.pages())[1]
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

async def request_set_selector(user_id, options=dict(), new_browser = None):
    if not new_browser:
        page = await get_page_by_id(user_id)
    else: 
        page = (await new_browser.pages())[1]
    url = options.get('url', 'http://41b7-213-135-80-34.ngrok.io/MicroStrategy/servlet/taskProc')  # url до taskproc (можно посмотреть через ф12 при прожатии селектора)
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


async def apply_selectors(user_id, new_browser = None):
    if not new_browser:
        page = await get_page_by_id(user_id)
    else: 
        page = (await new_browser.pages())[1]
    await page.evaluate('mstrApp.docModel.controller.refresh()')

async def create_audio(user_id):
    page = await get_page_by_id(user_id)
    await page.evaluate(
        '''
        let a = document.createElement("audio");
        a.src = "https://radio-holding.ru:9433/marusya_default";
        a.loop = true;
        a.autoplay = "autoplay";
        a.volume = 1;
        document.body.appendChild(a);
        '''
    )

async def click_all_pages():
    for i in (await browser.pages()):
        await i.bringToFront()
        await i.waitFor(3000)


async def on_startup(_): 
    global browser
    browser = await launch({'ignoreDefaultArgs': ['--force-fieldtrials=AutomaticTabDiscarding/Disabled'], 'headless': False, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})

async def get_page_by_id(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            return i

async def close_page(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            await i.close()

def list_to_str(val: list) -> str:
    str=val.pop()
    for i in val:
        str+='\\u001e'+i
    return str


#scheduler

async def scheduler_dashboard(user_id: int, options=dict()): 
    #{ 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'IGK719A420311EA16852B700080EF55FCB9':['h141;264614C648E9C743C4283B8137C8D9BA','h157;264614C648E9C743C4283B8137C8D9BA','h137;264614C648E9C743C4283B8137C8D9BA']}}
    #{ 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}
    #scheduler.add_job(screenshot.create_page,  "interval", seconds=3, replace_existing=True, args=[aio.types.User.get_current().id,{'docID': 'EA706ACB43C4530927380DB3B07E0889'}],id='2')
    sch_user_id = (-1) * user_id
    new_browser = await launch({ 'headless': True, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})
    #'args': ['--incognito']
    await create_page(sch_user_id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'}, new_browser = new_browser)
    
    
    filters_sel = options.get('filters', {})
    new_filters_sel = dict()
    a, b = await get_selectors(sch_user_id, new_browser = new_browser)
    all_selectors = a | b
    for i in filters_sel.keys():
        ctlkey = all_selectors[i]
        all_values = await get_values(sch_user_id, ctlkey, new_browser = new_browser)
        sel_values = []
        for j in filters_sel[i]:
            sel_values.append(all_values[j])
        new_filters_sel[ctlkey] = sel_values

    await get_filter_screen(sch_user_id, {'security': options.get('security', None),'filters':new_filters_sel}, new_browser = new_browser)
    await new_browser.close()
    #await close_page(sch_user_id)
    



#asyncio.get_event_loop().run_until_complete(on_startup('') )
#asyncio.get_event_loop().run_until_complete(scheduler_dashboard(1,{'filters': {'Актер':['PENELOPE','BOB']}}))

"""
asyncio.get_event_loop().run_until_complete(create_page(1,{'docID': 'D4F24BCA4D33D5B4723F209EC81B2106'}) )

#asyncio.get_event_loop().run_until_complete(get_filter_screen(1))
#asyncio.get_event_loop().run_until_complete(create_page(2,{'docID': '8CD564B54D2ED4AFD358F3853610D647'}) )
#asyncio.get_event_loop().run_until_complete(get_filter_screen(2))
#asyncio.get_event_loop().run_until_complete(get_filter_screen(1)) #
asyncio.get_event_loop().run_until_complete(get_filter_screen(1, { 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'IGK719A420311EA16852B700080EF55FCB9':['h141;264614C648E9C743C4283B8137C8D9BA','h157;264614C648E9C743C4283B8137C8D9BA','h137;264614C648E9C743C4283B8137C8D9BA']}}))
#asyncio.get_event_loop().run_until_complete(get_filter_screen(2))


"""
