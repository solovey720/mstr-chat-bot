from webdriver.screenshot import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///database/jobs.sqlite')
        }

scheduler = AsyncIOScheduler(jobstores=jobstores)
scheduler.start()
################################
scheduler.remove_all_jobs()
################################

#scheduler.add_job(scheduler_dashboard,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr1.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr1', name='sec_withsec_withfiltr1')

async def scheduler_dashboard(user_id: int, options=dict()): 
    new_browser = await launch({ 'headless': True, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})
    page = (await new_browser.pages())[0]

    await create_page(user_id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'}, new_browser = page)
    
    
    filters_sel = options.get('filters', {})
    new_filters_sel = dict()
    a, b = await get_selectors(user_id, new_browser = page)
    all_selectors = a | b
    for i in filters_sel.keys():
        ctlkey = all_selectors[i]
        all_values = await get_values(user_id, ctlkey, new_browser = page)
        sel_values = []
        for j in filters_sel[i]:
            sel_values.append(all_values[j])
        new_filters_sel[ctlkey] = sel_values

    await send_filter_screen(user_id, {'path_screenshot': options.get('path_screenshot', f'{user_id}.png'),'security': options.get('security', None),'filters':new_filters_sel}, new_browser = page)
    await new_browser.close()
    
def get_user_jobs(user_id: str):
    job_list=[]
    for job in scheduler.get_jobs():
        if job.id.startswith(user_id):
            job_list.append(job)
    return job_list

def get_jobs_name(jobs):
    job_name=[]
    for job in jobs:
        job_name.append(job.name)
    return job_name
