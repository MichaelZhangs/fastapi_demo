from fastapi import FastAPI
import os
from enum import IntEnum

api = FastAPI()

class BaseConfig(object):
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(ROOT, 'logs')
    LOG_NAME = os.path.join(LOG_DIR, 'test.log')

    SERVER_PORT = 7777

    # mock server
    MOCK_ON = False
    MOCK_PORT = 7778

    # MySQL连接信息
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "123456"
    DBNAME = "test"

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = "123456"

    # Redis连接信息
    REDIS_NODES = [{"host": REDIS_HOST, "port": REDIS_PORT, "db": REDIS_DB, "password": REDIS_PASSWORD}]

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, DBNAME)

    # 异步URI
    ASYNC_SQLALCHEMY_URI = f'mysql+aiomysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class DevConfig(BaseConfig):
    pass

class ProConfig(BaseConfig):
    pass

FAST_ENV =  os.environ.get("test", "dev")
Config = ProConfig() if FAST_ENV and FAST_ENV.lower() == "pro" else DevConfig()