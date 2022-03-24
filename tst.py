
from email import message
import requests
import asyncio

#request = requests.get('https://api.github.com')
#print(request.json()['current_user_url'])

from pyppeteer import launch
import logging
import re
#http://dashboards.corp.mvideo.ru/MicroStrategy/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=520F150011EB25866E6D0080EF154E9B&currentViewMedia=1&visMode=0&Server=MSTR-IS01.CORP.MVIDEO.RU&Project=%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0&Port=0&share=1&uid=administrator&pwd=Ceo143566!@
#LP 520F150011EB25866E6D0080EF154E9B
#log 84293CF411EB296FDA820080EFF566F0
#gfk 4E44AA6711EB13AC585C0080EFA5DBEF
#sales 52969EFC11EA3C7B42930080EF857558
#obs 0105984311EA440357CD0080EF354C4B



#https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb?evt=2048001&src=mstrWeb.2048001&documentID=520F150011EB25866E6D0080EF154E9B&currentViewMedia=1&visMode=0&Server=10.191.2.88&P
    

async def screenshot_html(options = dict()):

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
    path+='?evt=' + evt + '&src=mstrWeb.' + evt
    path+='&' + ( 'document' if options.get('docType', 'document') == 'dossier' else options.get('docType', 'document')) + 'ID=' + options.get('docID', '520F150011EB25866E6D0080EF154E9B') + '&currentViewMedia=1&visMode=0&'
    path+= 'Server=' + options.get('Server','MSTR-IS01.CORP.MVIDEO.RU') + '&'
    path+= 'Project=' + options.get('Project', '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0') + '&Port=0&share=1&'
    path+= 'uid=' + options.get('login', 'administrator') + '&' + 'pwd=' + options.get('password', 'Ceo143566!@')
    
##############
    
    '''
    path+='&evt=' + '1024001' + '&src=mstrWeb.' + 'oivm.rwb.1024001'
    path+='&events=-2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.WC5D6239510A84DC09D38527793A12086*.elemList*.h1;264614C648E9C743C4283B8137C8D9BA*.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0.2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.W5121A375615A451CA272FD10697EA8EA*.elemList*.h1;77ECA0D9445F155A4B08DFAC49FC9624*.elemList*.h23;77ECA0D9445F155A4B08DFAC49FC9624*.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0.2048014*.mstrWeb***.oivm***.rwb***.2048014_'
    path+='2048014*.mstrWeb***.oivm***.rwb***.2048014_&evtorder=2048001%2c1024001&2048001=1&1024001=1'
    '''
    '''
    path+='&evt=' + '1024001' + '&src=mstrWeb.' + 'oivm.rwb.1024001&events=-'
    for i in (цикл по фильтрам):
        
        sel_1 = '2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.' + ckey_1 +'*'
        val_1=''
        for j in (цикл по мультивыбору):
            val_1+='.elemList*.' + val + '*'
        sel_1+=val_1+'.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0.'
        path+=sel_1

    path+='2048014*.mstrWeb***.oivm***.rwb***.2048014_&evtorder=2048001%2c1024001&2048001=1&1024001=1'
    
    '''
    ####################################################
    browser = await launch({'headless': options.get('headless', True), 'ignoreHTTPSErrors': options.get('ignoreHTTPSErrors', True), 'defaultViewport': options.get('defaultViewport', {'width': 1920, 'height': 1080})})
    page = await browser.newPage()
    await page.goto(path, {'timeout':timeout_long})

    ############################ kostyl
    await page.waitForSelector('#\\33 054', {'timeout':timeout_long, 'visible': True} )
    await page.click('#\\33 054')    
    ############################

    selector_1 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType', 'document') == 'document') or (options.get('docType', 'document') == 'dossier') else ( '#UniqueReportID' if options.get('docType', 'document') == 'report' else 'ERROR')
    selector_2 = '#waitBox > div.mstrmojo-Editor.mstrWaitBox.modal' if (options.get('docType', 'document') == 'document') or (options.get('docType', 'document') == 'dossier') else ( '#divWaitBox' if options.get('docType', 'document') == 'report' else 'ERROR')

    
    try:
        #await page.waitForSelector(selector_1, {'timeout':timeout_long, 'visible': True} ) #ждем ухода самой загрузки документа и появления загрузки данных борда
        #await page.waitForSelector(selector_2, {'timeout':timeout_long, 'hidden': True} ) # ждем пока пропадет окно загрузки данных
        await page.waitFor(1000)
        for i in range(5): # Проверяем на фантомную пропажу окна загрузки. Если окно загрузки не появляется 3 сек, делаем скрин и выходим из цикла. иначе ждем менее 60 секунд, пока окно пропадет и возвращаемся в цикл
            try :
                await page.waitForSelector(selector_2, {'timeout':timeout_short, 'visible': True} )
            except:
                await page.screenshot({'path': options.get('path_screenshot', 'screenshots/example.png')})
                HTML = await page.evaluate('document.body.innerHTML')
                break
            await page.waitForSelector(selector_2, {'timeout':timeout_long, 'hidden': True} )
    except Exception as e:
        logging.exception(e)
        print('error')
    
    
    
    selectors = get_selectors(HTML)
    #print(selectors)
    tst= get_values(HTML, selectors['Актер'])
    #print(tst)

    '''await page.waitFor(7000)

    dat={
        'taskId': 'mojoRWManipulation',
        'rwb': rwb,
        'messageID': mid,
        'stateID': -1,
        'params': '{"actions":[{"act":"setSelectorElements","keyContext":"1\\u001eFB6800136946D43C790FA595F273FB404\\u001eW5121A375615A451CA272FD10697EA8EA","ctlKey":"W5121A375615A451CA272FD10697EA8EA","elemList":"h3;77ECA0D9445F155A4B08DFAC49FC9624;3:ADAPTATION HOLES","isVisualization":false,"include":true,"tks":"W12390BF5EDEF41D8A507193CEF784240"}],"partialUpdate":{"selectors":["W5121A375615A451CA272FD10697EA8EA"]},"style":{"params":{"treesToRender":3},"name":"RWDocumentMojoStyle"}}'
    }
    #print(dat)
    r =  requests.post('http://localhost:8080/MicroStrategy/servlet/taskProc', params=dat)
    
    print(r)'''

    
    
    await request_set_selector(page)
    await request_set_selector(page,{'ctlKey':selectors['Актер'],'elemList':tst['9:JOE']+'\\u001e'+tst['10:CHRISTIAN']}) 
    await trigger_selectors(page)


    await page.waitFor(3000000)
    return HTML

def get_selectors(HTML):

    select=dict()
    find_111 = HTML.find('\"t\":111') + 1
    while find_111 != 0:
        HTML = HTML[find_111:]
        HTML = HTML[HTML.find('\"n\":\"')+5:]
        name = HTML[:HTML.find('\"')]
        HTML = HTML[HTML.find('\"ckey\":\"')+8:]
        ckey = HTML[:HTML.find('\"')]
        select[name]=ckey
        find_111 = HTML.find('\"t\":111') + 1
    return select


def get_values(HTML, ckey):
    val=dict()
    HTML = HTML[HTML.find('\"k\":\"'+ ckey +'\"'):]
    begin = HTML.find('\"elms\":[') + 9
    end = HTML[begin:].find(']') - 1
    values = HTML[begin:begin + end].split('},{')
    for i in values:
        tmp = i
        tmp = tmp[tmp.find('\"v\":\"')+5:]
        value = tmp[:tmp.find('\"')]
        tmp = tmp[tmp.find('\"n\":\"')+5:]
        name = tmp[:tmp.find('\"')]
        val[name] = value
    return val

async def request_set_selector(page, options = dict()):
    taskid=options.get('taskid', 'mojoRWManipulation')
    rwb = await page.evaluate('mstrApp.docModel.bs')
    messageID = await page.evaluate('mstrApp.docModel.mid')
    ctlKey=options.get('ctlKey', 'W5121A375615A451CA272FD10697EA8EA')
    keyContext=await page.evaluate(f'mstrApp.docModel.getNodeDataByKey("{ctlKey}").defn.ck')
    elemList=options.get('elemList', 'h30;77ECA0D9445F155A4B08DFAC49FC9624')
    await page.evaluate(f'''
    url = 'http://localhost:8080/MicroStrategy/servlet/taskProc'
   
    fetch(url, {{
    method: 'POST',
        headers: {{
        'Content-type': 'application/x-www-form-urlencoded',
        }},
    body:"taskId={taskid}&rwb={rwb}&messageID={messageID}&stateID=-1&params=%7B%22actions%22%3A%5B%7B%22act%22%3A%22setSelectorElements%22%2C%22keyContext%22%3A%22{keyContext}%22%2C%22ctlKey%22%3A%22{ctlKey}%22%2C%22elemList%22%3A%22{elemList}%22%2C%22isVisualization%22%3Afalse%2C%22include%22%3Atrue%2C%22tks%22%3A%22W12390BF5EDEF41D8A507193CEF784240%22%7D%5D%2C%22partialUpdate%22%3A%7B%22selectors%22%3A%5B%22W5121A375615A451CA272FD10697EA8EA%22%5D%7D%2C%22style%22%3A%7B%22params%22%3A%7B%22treesToRender%22%3A3%7D%2C%22name%22%3A%22RWDocumentMojoStyle%22%7D%7D&zoomFactor=1&styleName=RWDocumentMojoStyle&taskContentType=json&taskEnv=xhr&xts="+ mstrmojo.now() +"&mstrWeb="+mstrApp.servletState
    }})   
    ''')

async def trigger_selectors(page, sel_name='Selector3e8'):
    await page.click('#mstrHamburger')   
    await page.evaluate('document.querySelector(\'a[class="item rerun"]\').click()')

    # await page.evaluate(f"document.querySelector('div[nm=\"{sel_name}\"]').querySelector('div[aria-label=\"OK\"]').click()")
    
    '''await page.evaluate(f\'\'\'
    z=document.querySelectorAll('div[class="mstrmojo-DocSelector"] .mstrmojo-Button-text')
    for (let i = 0; i < z.length; i++) {{ 
        console.log(z[i]);
    if (z[i].innerText==='OK') {{z[i].click(); break;}}
    }}
    \'\'\')
    '''


#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'52969EFC11EA3C7B42930080EF857558','docType': 'document'}))
#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'743FFE22314887C8F2407C9B559ECB4C','docType': 'dossier','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))
#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'233DB69981444C2B38E266AF39289366','docType': 'document','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))
#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'2D189DE4CE4C01EF63C980A85CDE53A5','docType': 'report', 'path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))

asyncio.get_event_loop().run_until_complete(screenshot_html({'timeout_short':1000, 'headless': False,'docID':'A76ADD394EC610BD76FFBCBE03023721','docType': 'document','path': 'http://localhost:8080/MicroStrategy/servlet/mstrWeb' ,'Server':'DESKTOP-2RSMLJR', 'Project': 'New+Project', 'password':'','defaultViewport': {'width': 800, 'height': 600}}))
