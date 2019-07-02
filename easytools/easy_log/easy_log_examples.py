#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2016/10/29 下午9:32


import time

from EasyTools.easytools.easy_log.easy_log import EasyLog


def example1():
    logger = EasyLog("my_module")

    for i in xrange(1, 16):
        logger.error("critical message %s" % i)
        time.sleep(1)

def example2():
    """
        test email
        将日志打印到控制台和发送到指定邮箱
    :return:
    """
    try:
        1 / 0
    except Exception, e:
        logger = EasyLog("my_module")
        logger.critical(e)


if __name__ == "__main__":
    example2()



