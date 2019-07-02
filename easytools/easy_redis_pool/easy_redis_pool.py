#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2016/12/17 上午10:35

import redis

config = {
    'default': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0
    }
}


class MyRedisPool:
    """
        redis连接池
    """
    _redis_pool = {}

    def __init__(self):
        pass

    @staticmethod
    def get_instance(redis_name='default'):     # 可增加一个名字参数，根据该参数加载对应的配置
        """
            单例模式
        :return:
        """
        if not config.get(redis_name):
            return None

        host = config.get(redis_name).get('host')
        port = config.get(redis_name).get('port')
        db = config.get(redis_name).get('db')

        key = host + str(port)
        if not MyRedisPool.redis.get(key):
            if not host:
                raise IOError('error: host is null!')
            try:
                port = int(port)
            except:
                raise TypeError('error: port must be integer!')

            try:
                MyRedisPool.redis[key] = redis.StrictRedis(host=host, port=port, db=db)
            except:
                raise IOError('error: connect error!')

        return MyRedisPool.redis.get(key)


if __name__ == '__main__':
    host = '10.60.81.83'
    password = ''
    port = 6379
    r = MyRedisPool.get_instance(host, port)
    r.hset('key', 'a', 'b')
    print r.hget('key', 'a')

