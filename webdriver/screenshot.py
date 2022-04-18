from webdriver.page_interaction import *
from create_bot_and_conn import bot, SERVER_LINK, LOGIN, PASSWORD, PROJECT, SERVER
from aiogram.types import InputFile
import logging
import os

import asyncio

run_limit = 10

sem = asyncio.Semaphore(run_limit)



async def _sem_create_page(user_id, options=dict(), new_browser = None):


    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)
    path = options.get('path', f'{SERVER_LINK}/MicroStrategy/servlet/mstrWeb') # https://dashboard-temp/MicroStrategy/servlet/mstrWeb
    docID = options.get('docID', 'C4DB9BA7BF457B5B6D345090FF2BA99F')
    docType = options.get('docType', 'document')
    server = options.get('Server', SERVER)
    project = options.get('Project', PROJECT)
    login = options.get('login', LOGIN)
    password = options.get('password', PASSWORD)
    headless = options.get('headless', True)

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
        page = await create_browser(user_id, headless = headless)
    else: 
        page = new_browser
    

    page.user_id = user_id

    await page.goto(path, {'timeout': timeout_long})
    ############################ press 'continue'
    #await page.waitForSelector('#\\33 054', {'timeout': timeout_long,'visible': True})
    #await page.click('#\\33 054')
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
    
async def create_page(user_id, options=dict(), new_browser = None): 
    """Create new browser.

    Available options are:

    * ``user_id`` (int): userID from TG
    * ``timeout_long`` (int): Maximum navigation time in milliseconds
    * ``timeout_short`` (int): Maximum download time in milliseconds
    * ``path`` (str): path to the MstrWeb
    * ``docID`` (str): id of the opening document
    * ``docType`` (str): type of the document
    * ``server`` (str): Mstr server name
    * ``project`` (str): Mstr project name
    * ``login`` (str): Mstr login
    * ``password`` (str): Mstr password
    * ``evt`` (str): Mstr event (use default to document, report, dossier)

    await create_page(aio.types.User.get_current().id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'})
    """ 
    async with sem:
        #print('start create')
        await _sem_create_page(user_id, options, new_browser)


async def _sem_send_filter_screen(user_id, options=dict(), new_browser = None, is_ctlkey = True):
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)
    docType = options.get('docType', 'document')
    screen_name = options.get('path_screenshot', f'{user_id}.png')

    security_sel = 'S_security'
    security_val = options.get('security', [])

    filters_sel = options.get('filters', {})

    if not (security_val or filters_sel):
        await page.screenshot({'path': screen_name})
        await bot.send_document(chat_id=user_id, document=InputFile(screen_name))
        os.remove(screen_name)
        return

    a, b = await get_selectors(user_id, new_browser=page)
    all_selectors = a | b

    try:
        if security_val:
            ctlkey = (all_selectors)[security_sel]
            tmp = await get_values(user_id, ctlkey, new_browser=page)
            security_ctl_val=[]
            for i in security_val:
                security_ctl_val.append(tmp[i])
            await request_set_selector(user_id, {'ctlKey': f'{ctlkey}', 'elemList': list_to_str(security_ctl_val)}, new_browser=page)
    except:
        return

    try:
        if filters_sel: 
            if is_ctlkey:    
                for i in filters_sel.keys():
                    await request_set_selector(user_id, {'ctlKey': i, 'elemList': list_to_str(filters_sel[i])}, new_browser=page)
            else:
                for i in filters_sel.keys():
                    ctlkey = (all_selectors)[i]
                    tmp = await get_values(user_id, ctlkey, new_browser=page)
                    ctl_val=[]
                    for j in filters_sel[i]:
                        ctl_val.append(tmp[j])
                    await request_set_selector(user_id, {'ctlKey': f'{ctlkey}', 'elemList': list_to_str(ctl_val)}, new_browser=page)
    except:
        print('filter error')

        
    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (docType == 'dossier') else (
        '#UniqueReportID' if docType == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (docType == 'document') or (docType == 'dossier') else (
        '#divWaitBox' if docType == 'report' else 'ERROR')
    
    await apply_selectors(user_id, new_browser=page)
 
    try:
        await page.waitForSelector(selector_1, {'timeout': timeout_long, 'visible': True})  # ждем ухода самой загрузки документа и появления загрузки данных борда
        await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})  # ждем пока пропадет окно загрузки данных
        for i in range(5):  # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
            try:
                await page.waitForSelector(selector_2, {'timeout': timeout_short, 'visible': True})
            except:
                await page.screenshot({'path': screen_name})
                await bot.send_document(chat_id=user_id, document=InputFile(screen_name))
                os.remove(screen_name)
                return 
            await page.waitForSelector(selector_2, {'timeout': timeout_long, 'hidden': True})
    except Exception as e:
        logging.exception(e)
        print('error')
    
    return 

async def send_filter_screen(user_id, options=dict(), new_browser = None, is_ctlkey = True):  
    """Send screenshot of the document with filters

    Available options are:

    * ``user_id`` (int): userID from TG
    * ``timeout_long`` (int): Maximum navigation time in milliseconds
    * ``timeout_short`` (int): Maximum download time in milliseconds
    * ``path_screenshot`` (str): path to save screenshot
    * ``security`` (list): values to apply of security selector 
    * ``filters`` (dict): dict of ``selector``(str): ``values id``(list) to apply  
    * ``docType`` (str): type of the document

    await send_filter_screen(aio.types.User.get_current().id)
    await send_filter_screen(aio.types.User.get_current().id, {'path_screenshot':f'{aio.types.User.get_current().id}_sec_withsec_withfiltr.png','filters': {'Актер':['PENELOPE','BOB'], 'Год':['2006']}}, is_ctlkey=False)
    await send_filter_screen(aio.types.User.get_current().id, {'path_screenshot':f'{aio.types.User.get_current().id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB'], 'Год':['2006']}}, is_ctlkey=False)
    await send_filter_screen(aio.types.User.get_current().id, {'path_screenshot':f'{aio.types.User.get_current().id}_sec_withsec_withfiltr.png','filters': {'IGK719A420311EA16852B700080EF55FCB9':['h4;264614C648E9C743C4283B8137C8D9BA','h5;264614C648E9C743C4283B8137C8D9BA'], 'IGK719A442911EA16852B700080EF55FCB9':['h2006;F65860F746DE5329EC4065B6F888ED7D']}})
    """ 
    async with sem:
        #print('start send')
        await _sem_send_filter_screen(user_id, options, new_browser = new_browser, is_ctlkey = is_ctlkey)