import asyncio
import datetime
import time

from config.configs import Config
from log.logger import Log
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request, Response
from app.routers import api
from fastapi.middleware.cors import CORSMiddleware
from app.config.database_config import async_session
from utils.redis_help import redis_conn
from log.new_log import create_logger, stdout_handler, daily_rotaiting_handler



api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = async_session()
        response = await call_next(request)
    finally:
       await request.state.db.close()
    return response

@api.on_event('startup')
def init_scheduler():
    """
    初始化定时任务
    :return:
    """
    # SQLAlchemyJobStore指定存储链接
    job_store = {
        'default': SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI, engine_options={"pool_recycle": 1500},
                                      pickle_protocol=3)
    }
    api.scheduler = AsyncIOScheduler()
    api.scheduler.configure(jobstores=job_store)
    api.scheduler.start()
    api.logger = Log()
    api.logger.info("ApScheduler started success.        ✔")

    api.new_log = create_logger("", (daily_rotaiting_handler(filename="./logs/new_log.log"), stdout_handler()))
    api.new_log.info("新的日志打印来了")


def f():
    print("hello FastApi .......")
    redis_conn.set("f_func", "1")
    api.logger.error("hello FastApi .......")
    api.logger.info("嘿嘿嘿额嘿嘿")

def g():
    print("hahahahha.......")
    redis_conn.set("g_func", "1")
    api.logger.warning("hahahahha.......")
    api.logger.debug("哈哈哈哈哈哈哈哈")

@api.on_event('startup')
def aps_scheduler():
    api.logger.debug(f"开始初始化定时任务......")
    # f_v = redis_conn.get("f_func")
    # g_v = redis_conn.get("g_func")
    # 启动前检查是否有定时任务
    jobs = api.scheduler.get_jobs()
    cur_time = str(datetime.datetime.now())
    if jobs:
        for job in jobs:
            t = str(job.next_run_time)
            if "." in t:
                t0 = t.split(".")[0]
                date_t0 = datetime.datetime.strptime(t0, "%Y-%m-%d %H:%M:%S")
                if cur_time > str(date_t0 + datetime.timedelta(minutes=5)):
                    api.scheduler.resume_job(job.id)
                print(job.id, job.name)

    else:
        api.scheduler.add_job(f, "interval", minutes=5,  id=str(id(f)))
        api.scheduler.add_job(g, "interval", minutes=3, id=str(id(g)))
