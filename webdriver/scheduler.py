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


async def scheduler_dashboard(user_id: int, options=dict()): 
    #{ 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'IGK719A420311EA16852B700080EF55FCB9':['h141;264614C648E9C743C4283B8137C8D9BA','h157;264614C648E9C743C4283B8137C8D9BA','h137;264614C648E9C743C4283B8137C8D9BA']}}
    #{ 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}
    #scheduler.add_job(screenshot.create_page,  "interval", seconds=3, replace_existing=True, args=[aio.types.User.get_current().id,{'docID': 'EA706ACB43C4530927380DB3B07E0889'}],id='2')
    #sch_user_id = (-1) * user_id
    new_browser = await launch({ 'headless': True, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})
    #'args': ['--incognito']
    await create_page(user_id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'}, new_browser = new_browser)
    
    
    filters_sel = options.get('filters', {})
    new_filters_sel = dict()
    a, b = await get_selectors(user_id, new_browser = new_browser)
    all_selectors = a | b
    for i in filters_sel.keys():
        ctlkey = all_selectors[i]
        all_values = await get_values(user_id, ctlkey, new_browser = new_browser)
        sel_values = []
        for j in filters_sel[i]:
            sel_values.append(all_values[j])
        new_filters_sel[ctlkey] = sel_values

    await get_filter_screen(user_id, {'path_screenshot': options.get('path_screenshot', f'{user_id}.png'),'security': options.get('security', None),'filters':new_filters_sel}, new_browser = new_browser)
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
