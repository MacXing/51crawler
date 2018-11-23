# -*- coding: utf-8 -*- 
# @Time : 2018/11/23 11:32 
# @Author : Allen 
# @Site :  日志模块

import logging
import datetime


class Log:
    def __init__(self):
        self.logger = logging.getLogger()
        self.LOG_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.file_handel = logging.FileHandler('../log/crawl.log', encoding='utf-8')
        self.file_handel.setFormatter(self.LOG_FORMAT)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handel)

    def get_logger(self):
        self.start()
        return self.logger

    def start(self):
        self.logger.info('*' * 25)
        self.logger.info("Star:" + datetime.datetime.now().strftime("%Y-%m-%d"))
        self.logger.info('*' * 25)


if __name__ == '__main__':
    logger = Log().get_logger()
