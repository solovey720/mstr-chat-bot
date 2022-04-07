from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///database/jobs.sqlite')
        }
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
Scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors)
Scheduler.start()


#jobstore = SQLAlchemyJobStore(url='sqlite:///database/jobs.sqlite')
#executor = ProcessPoolExecutor(5)
#scheduler = BackgroundScheduler(jobstores=jobstore, executors=executor)

