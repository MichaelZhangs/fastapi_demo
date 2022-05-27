import inspect
import os

from loguru import logger

from config.configs import Config

class Log():
    business = None

    def __init__(self, name='test'):  # Logger标识默认为app
        """
        :param name: 业务名称
        """
        # 如果目录不存在则创建
        if not os.path.exists("./logs/"):
            os.mkdir("./logs/")
        self.business = name
        print(Config.LOG_DIR + "/" +"/{time:YYYY-MM-DD}.log")
        logger.add( "./logs/"+ "/{time:YYYY-MM-DD}.log", rotation="10 MB")
    def info(self, message: str):
        print("---info----")
        logger.info(message)

    def error(self, message: str):
        logger.error(message)

    def warning(self, message: str):
        logger.warning(message)

    def debug(self, message: str):
        logger.debug(message)

    def exception(self, message: str):
        logger.exception(message)