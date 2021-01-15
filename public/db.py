# -*- coding: utf-8 -*-
# @File: db.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/11/9  17:55


import pymysql
import cx_Oracle
import redis
from rediscluster import RedisCluster

from config.setting import MYSQL, ORACLE, REDIS, REDIS_CLUSTER, REDIS_CLUSTER_PASWORD
from public.logs import logger


class Mysql:
    """
    mysql 操作类
    """

    @staticmethod
    def connMysql():
        """
        Mysql 连接
        :return:  str  Mysql连接串
        """
        try:
            conn = pymysql.connect(**MYSQL)
            return conn
        except Exception as e:
            logger.error(f'Mysql客户端连接失败! {e}')

    @staticmethod
    def select(sql):
        """
        SQL 操作
        :param sql:  str sql
        :return:  tupe
        """
        try:
            conn = Mysql.connMysql()
            cur = conn.cursor()
            cur.execute(sql)
            select_data = cur.fetchall()
            cur.close()
            conn.close()
            return select_data
        except Exception as e:
            logger.error(f'执行Mysql sql错误{e}')


class Oracle:
    """
    Oracle 操作类
    """

    @staticmethod
    def connOracle():
        """
        Oracle 连接客户端
        :return:
        """
        try:
            info = list(ORACLE.values())
            db = cx_Oracle.connect(f'{info[0]}/{info[1]}@{info[2]}')
            cursor = db.cursor()
            return cursor
        except Exception as e:
            logger.error(f'连接Oracle客户端错误!{e}')

    @staticmethod
    def select(sql):
        """
        Oracle sql 执行
        :param sql:  sql str
        :return: tupe
        """
        try:
            conn = Oracle.connOracle()
            conn.execute(sql)
            select_data = conn.fetchall()
            conn.close()
            return select_data
        except Exception as e:
            logger.error(f'执行Oracle sql异常{e}')


class RedisPool:
    """
    redis 操作类    可直接 re = RedisPool()   re.session.xx() 以下封装方法有限

    """
    __Pool = None

    def __init__(self):

        self.session = self.get_conn()

    @staticmethod
    def get_conn():
        if not RedisPool.__Pool:
            RedisPool.__Pool = redis.ConnectionPool(host=REDIS.get('host'), port=REDIS.get('port'),
                                                    password=REDIS.get('password'), db=REDIS.get('db'))

        session = redis.StrictRedis(connection_pool=RedisPool.__Pool)
        return session


    def set(self, key, value):
        """
        redis  set 操作
        :param key: 键
        :param value: 值
        :return:
        """
        ret = self.session.set(key, value)
        self.session.close()
        return ret

    def get(self, key):
        """
        redis get 操作
        :param key: 键
        :return:
        """

        vlaue = self.session.get(key)

        self.session.close()
        if vlaue != None:
            return vlaue
        else:
            return '无此键！'



class RedisClusterDb():
    """
    redsi 集群操作类
    """

    @staticmethod
    def connect():
        """
        连接redis集群
        :return: object
        """
        try:
            redisconn = RedisCluster(startup_nodes=REDIS_CLUSTER, password=REDIS_CLUSTER_PASWORD)
            return redisconn
        except Exception as e:
            logger.error(f"错误,连接redis 集群失败 {e}")
            return False

    @staticmethod
    def set(key, value):
        """
        redis  set 操作
        :param key: 键
        :param value: 值
        :return:
        """
        ret = RedisClusterDb.connect().set(key, value)
        RedisClusterDb.connect().close()
        return ret

    @staticmethod
    def get(key):
        vlaue = RedisClusterDb.connect().get(key)
        if vlaue != None:
            return vlaue
        else:
            return '无此键！'

