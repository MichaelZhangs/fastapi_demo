import asyncio
from config.configs import Config
from log.logger import Log
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request, Response
from app.routers import api
from fastapi.middleware.cors import CORSMiddleware
from app.config.database_config import async_session


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
    api.scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
    api.scheduler.configure(jobstores=job_store)
    api.scheduler.start()
    api.logger = Log()
    api.logger.info("ApScheduler started success.        ✔")
