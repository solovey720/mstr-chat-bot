from webdriver.screenshot import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import asyncio

run_limit = 5

sem = asyncio.Semaphore(run_limit)

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///database/jobs.sqlite')
        }

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Europe/Moscow")
scheduler.start()
################################
scheduler.remove_all_jobs()
################################
#######################################################################Примеры запусков
#scheduler.add_job(sem_scheduler_dashboard, "cron", day_of_week='mon-sun', hour=17, minute=27, misfire_grace_time = None, replace_existing=True, args=[user_id, {'docID': '18C63CAE4B8268E07E3DAEA5E275BCC3', 'path_screenshot':f'{user_id}_sec_withsec_withfilt{i}r.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfil{i}tr', name=f'sec_withsec_wi{i}thfiltr')  

#scheduler.add_job(scheduler_dashboard,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr1.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr1', name='sec_withsec_withfiltr1')
#scheduler.add_job(scheduler_dashboard, "cron", day_of_week='mon-sun', hour=15, minute=44, misfire_grace_time = None, replace_existing=True, args=[user_id, {'docID': '18C63CAE4B8268E07E3DAEA5E275BCC3', 'path_screenshot':f'{user_id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr', name=f'sec_withsec_withfiltr')

async def scheduler_dashboard(user_id: int, options=dict()): 
    new_browser = await launch({ 'headless': True, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})
    page = (await new_browser.pages())[0]
    sched_options = options.copy()

    await create_page(user_id, options = sched_options, new_browser = page)
    
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

    sched_options['filters'] = new_filters_sel
    await send_filter_screen(user_id, options = sched_options, new_browser = page)
    await new_browser.close()
    
async def sem_scheduler_dashboard(user_id: int, options=dict(), i=1):     
    async with sem:
        await scheduler_dashboard(user_id, options)


def get_user_jobs(user_id: str):
    job_list=[]
    for job in scheduler.get_jobs():
        if job.id.startswith(user_id):
            job_list.append(job)
    return job_list

def delete_job (job_id):
    scheduler.remove_job(job_id)

def get_jobs_name(jobs):
    job_name=[]
    for job in jobs:
        job_name.append(job.name)
    return job_name
