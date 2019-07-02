#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2016/12/17 上午10:27

import MySQLdb
from DBUtils.PooledDB import PooledDB
import torndb
from time import sleep


Host = "127.0.0.1"
User = "root"
Passwd = "root"
Db = "xx"
Port = 3306


class MyDBPool:
    """
        连接池类, 使用了单例模式
    """
    pool_instance = None
    conn_pool = None

    def __init__(self):
        max_connection = 5
        self.conn_pool = PooledDB(MySQLdb, max_connection, host=Host, user=User, passwd=Passwd, db=Db, port=Port)

    @staticmethod
    def get_instance():     # 可以增加一个参数：根据dbname来加载对应的配置文件
        MyDBPool.pool_instance = MyDBPool.pool_instance or MyDBPool()
        return MyDBPool.pool_instance.get_connect()

    def get_connect(self):
        return self.conn_pool.connection()


class MyDB:
    """
        获取数据库连接, 使用torndb
    """
    db = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():     # 可以增加一个参数：根据dbname来加载对应的配置文件
        try:
            db = torndb.Connection(Host + ":" + str(Port), Db, user=User, password=Passwd)
        except Exception, e:
            print e
            db = None
        return db


if __name__ == "__main__":
    # db_connection = MyPool.get_instance()
    db_connection = MyDB.get_instance()
    # print db_connection
    sleep(10)

    # TODO
    # 这个类只能建立一个数据库的连接池对象，实际使用时可能需要多个，可以参考easy_redis_pool

