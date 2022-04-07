
import asyncio
import secrets
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///database/jobs.sqlite')
        }
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
scheduler = AsyncIOScheduler(jobstores=jobstores) #, executors=executors
scheduler.start()
#scheduler.remove_all_jobs()
user_id='12_3'
async def job(txt):
    print(txt)



scheduler.add_job(job,  "interval", seconds=3, replace_existing=True, args=['a'],id=user_id, name='qwerqwerqwerqerqwerqweqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerqwerw')

def get_user_jobs(user_id: str):
    job_list=[]
    for job in scheduler.get_jobs():
        if job.id.startswith(user_id):
            job_list.append(job)
    return job_list

#print(scheduler.get_jobs(jobstore='12'))

def get_jobs_name(jobs):
    job_name=[]
    for job in jobs:
        job_name.append(job.name)
    return job_name
print(*get_jobs_name(get_user_jobs('12')))

asyncio.get_event_loop().run_forever()
#jobstore = SQLAlchemyJobStore(url='sqlite:///database/jobs.sqlite')
#executor = ProcessPoolExecutor(5)
#scheduler = BackgroundScheduler(jobstores=jobstore, executors=executor)

