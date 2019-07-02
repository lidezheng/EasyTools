#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2016/12/17 上午10:35

import os


def ping(host, timeout=500):
    """
    :param host: 主机名
    :param timeout: 超时时间，100ms
    :return: 能ping通 True， 超时或ping不通 False
    """
    command = "ping -c 1 " + host + " -W " + str(timeout) + " > /dev/null 2>&1"
    response = os.system(command)
    print response
    if response == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    urls = ["www.baidu111aa11.com", "www.baidu.com", "www.google.com"]
    for url in urls:
        if ping(url):
            print url, "UP"
        else:
            print url, "DOWN"
