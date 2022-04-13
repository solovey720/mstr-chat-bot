from pyppeteer import launch
from pyppeteer.page import Page
from create_bot_and_conn import server_link
#from webdriver.start_browser import *

_browsers_list = dict()

async def create_browser(user_id: int, headless = True) -> Page:
    _browsers_list[user_id] = await launch({ 'headless': headless, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})
    page = (await _browsers_list[user_id].pages())[0]
    return page 

async def close_browser(user_id: int):
    _browsers_list[user_id].close()
    _browsers_list.pop(user_id)
   
async def get_browsers_page(user_id: int) -> Page:
    page = (await _browsers_list[user_id].pages())[0]
    return page
   



async def get_selectors(user_id, new_browser = None):
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

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
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

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
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

    url = options.get('url', f'{server_link}/MicroStrategy/servlet/taskProc')  # url до taskproc (можно посмотреть через ф12 при прожатии селектора)
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
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

    await page.evaluate('mstrApp.docModel.controller.refresh()')


def list_to_str(val: list) -> str:
    str=val.pop()
    for i in val:
        str+='\\u001e'+i
    return str

"""
async def get_page_by_id(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            return i

async def close_page(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            await i.close()
"""