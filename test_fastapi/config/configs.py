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

    # 权限 0 普通用户 1 组长 2 管理员
    MEMBER = 0
    MANAGER = 1
    ADMIN = 2

    # github access_token地址
    GITHUB_ACCESS = "https://github.com/login/oauth/access_token"

    # github获取用户信息
    GITHUB_USER = "https://api.github.com/user"

    # client_id
    CLIENT_ID = "c46c7ae33442d13498cd"

    # SECRET
    SECRET_KEY = "6cb53ad7d135bb91a07f2deb7203d484741f1644"
    # 测试报告路径
    REPORT_PATH = os.path.join(ROOT, "templates", "report.html")

    # APP 路径
    APP_PATH = os.path.join(ROOT, "app")

    # dao路径
    DAO_PATH = os.path.join(APP_PATH, 'crud')

    # markdown地址
    MARKDOWN_PATH = os.path.join(ROOT, 'templates', "markdown")

    SERVER_REPORT = "http://localhost:8000/#/record/report/"

    OSS_URL = "http://oss.pity.fun"

    RELATION = "pity_relation"
    ALIAS = "__alias__"
    TABLE_TAG = "__tag__"
    # 数据库表展示的变更字段
    FIELD = "__fields__"
    SHOW_FIELD = "__show__"
    IGNORE_FIELDS = ('created_at', "updated_at", "deleted_at", "create_user", "update_user")

    # 测试计划中，case默认重试次数
    RETRY_TIMES = 1

    # 请求类型
    class BodyType(IntEnum):
        none = 0
        json = 1
        form = 2
        x_form = 3
        binary = 4
        graphQL = 5

    # 全局变量的类型
    class GconfigType:
        case = 0
        constructor = 1
        asserts = 2

        @staticmethod
        def value(val):
            if val == 0:
                return "用例"
            if val == 1:
                return "前后置条件"
            return "断言"

    # 前置条件类型
    class ConstructorType:
        testcase = 0
        sql = 1
        redis = 2
        py_script = 3
        http = 4

    # 日志类型
    class OperationType:
        INSERT = 0
        UPDATE = 1
        DELETE = 2
        EXECUTE = 3
        STOP = 4

    # 通知类型
    class NoticeType(IntEnum):
        EMAIL = 0
        DINGDING = 1
        WECHAT = 2
        FEISHU = 3

    # 日志名
    PITY_ERROR = "test_error"
    PITY_INFO = "test_info"

class DevConfig(BaseConfig):
    pass

class ProConfig(BaseConfig):
    pass

FAST_ENV =  os.environ.get("test", "dev")
Config = ProConfig() if FAST_ENV and FAST_ENV.lower() == "pro" else DevConfig()