#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2016/10/29 下午6:16


import logging
import logging.config
import yaml


class EasyLog:
    """
        日志类
    """

    @classmethod
    def config(cls, fullpath):
        try:
            with open(fullpath) as fd:
                content = yaml.load(fd)
            logging.config.dictConfig(content)
        except IOError as e:
            print "File error: " + str(e)

    def __init__(self, log_filename):
        self.logger = logging.getLogger(log_filename)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)


if __name__ == "__main__":
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))
    fullpath = os.path.join(dir_path, "easy_log.yaml")

    EasyLog.config(fullpath=fullpath)

    logger = EasyLog("my_module")

    logger.error("error message")
    logger.warn("warn message")

