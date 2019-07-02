#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2017/6/16 下午6:23


import time
import threading
from threading import Thread
import Queue


def concurrent_worker(arg):
    """任务处理函数worker"""
    time.sleep(arg)
    print(arg, threading.current_thread().getName())


def start_concurrent_worker():
    """启动多个worker(函数方式)"""
    threads = []
    for i in range(5):
        t = threading.Thread(target=concurrent_worker, args=(i+1,))
        t.setDaemon(False)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('done...')


class ConcurrentWorker(Thread):
    """worker类"""
    # 待处理公共队列
    queue = None

    def __init__(self, daemon=False, name=None, arg=None):
        self.arg = arg
        Thread.__init__(self, name=name)
        # threading.Thread.setName(self, name=name)
        Thread.setDaemon(self, daemon)

    def run(self):
        while True:
            time.sleep(self.arg)
            print(threading.current_thread().getName())
            if not ConcurrentWorker.queue:
                break


def start_class_worker():
    """启动多个worker(类方式)"""
    threads = []
    for i in range(5):
        t = ConcurrentWorker(name='Thread-{}'.format(i+1), arg=i+1)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print('done...')




def main():
    pass

if __name__ == '__main__':
    """实现多线程任务常用方式"""
    # 1. 函数式多worker
    # start_concurrent_worker()

    # 2. 类方式多worker
    start_class_worker()



    # 3. 函数式多consumer/producer
    # 4. 类方式多consumer/producer

    # 5. 共享全局queue
    # 6. 锁机制

    # 7. 多进程的实现方式
    # 8. 多进程常用结构