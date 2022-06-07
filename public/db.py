# -*- coding: utf-8 -*-
# @File: db.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/3/18  19:23

from typing import TypeVar, Tuple, List

import cx_Oracle
import pymysql
import redis
from rediscluster import RedisCluster

from public.common import logger,reda_conf


T = TypeVar('T')  # 可以是任何类型。


# 读取配置参数
DB = reda_conf('DB')
MYSQL = DB.get('MYSQL')
ORACLE = DB.get('ORACLE')
REDIS = DB.get('REDIS')
REDIS_CLUSTER = DB.get('REDIS_CLUSTER')
REDIS_CLUSTER_PASWORD = DB.get('REDIS_CLUSTER_PASWORD')


class Mysql:
    """
    mysql 操作类  demo  Mysql.select('SELECT * FROM `case`')
    """

    @classmethod
    def connMysql(cls) -> T:
        """
        Mysql 连接
        :return:  str  Mysql连接串
        """
        try:
            conn = pymysql.connect(**MYSQL)
            return conn
        except Exception as e:
            logger.error(f'Mysql客户端连接失败! {e}')

    @classmethod
    def select(cls, sql: str) -> Tuple or List:
        """
        SQL 操作   "select * from  `case`"
        :param sql:  str sql
        :return:  tupe
        """
        try:
            conn = cls.connMysql()
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
    Oracle 操作类  demo  Oracle.select('SELECT * FROM `case`')
    """

    @classmethod
    def connOracle(cls) -> T:
        """
        Oracle 连接客户端
        :return:
        """
        try:
            info = list(ORACLE.values())
            db = cx_Oracle.connect(f'{info[0]}/{info[1]}@{info[2]}')
            return db
        except Exception as e:
            logger.error(f'连接Oracle客户端错误!{e}')

    @classmethod
    def ex_select(cls, sql: str) -> Tuple or List:
        """ 查询
        Oracle sql 执行
        :param sql:  sql str
        :return: tupe
        """
        try:
            conn = cls.connOracle()
            cursor = conn.cursor()
            cursor.execute(sql)
            select_data = cursor.fetchall()
            cursor.close()
            conn.close()
            logger.debug('查询sql成功！！')
            return select_data
        except Exception as e:
            logger.error(f'执行Oracle 查询异常{e}')

    @classmethod
    def ex_insert(cls, sql: str) -> Tuple or List:
        """ 插入
        Oracle sql 执行
        :param sql:  sql str
        :return: tupe
        """
        try:
            conn = cls.connOracle()
            cursor = conn.cursor()

            cursor.execute(sql)
            conn.commit()

            cursor.close()
            conn.close()
            logger.debug('提交sql成功！！')
        except Exception as e:
            logger.error(f'执行Oracle 插入异常{e}')


class RedisPool:
    """
    redis 操作类    demo  re = RedisPool()  re.set('han','2019')  re.get('han')

    """
    __Pool = None

    def __init__(self):
        self.session = self.redis_conn()

    def redis_conn(self) -> T:
        """
        连接redis 操作
        :return:
        """
        try:
            if not RedisPool.__Pool:
                RedisPool.__Pool = redis.ConnectionPool(host=REDIS.get('host'), port=REDIS.get('port'),
                                                        password=REDIS.get('password'), db=REDIS.get('db'))

            session = redis.StrictRedis(connection_pool=RedisPool.__Pool)
            return session
        except Exception as e:
            logger.error(f'连接错误！{e}')

    def set(self, key: str, value: str) -> T:
        """
        redis  set 操作
        :param key: 键
        :param value: 值
        :return:
        """
        ret = self.session.set(key, value)
        self.session.close()
        return ret

    def get(self, key: str) -> T:
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
            logger.error('无此key')
            return None


class RedisPoolCluster:
    """
    redsi 集群操作类
    """

    def __init__(self):

        self.session = self.connect()

    def connect(self):
        """
        连接redis集群
        :return: object
        """
        try:
            redisconn = RedisCluster(startup_nodes=REDIS_CLUSTER, password=REDIS_CLUSTER_PASWORD)
            return redisconn
        except Exception as e:
            logger.error(f"错误,连接redis 集群失败 {e}")
            return None

    def set(self, key: T, value: T) -> T:
        """
        redis  set 操作
        :param key: 键
        :param value: 值
        :return:
        """
        set_key = self.session.set(key, value)
        self.session.close()
        return set_key

    def get(self, key: T) -> T:
        """
         获取指定键
        :param key:  key
        :return:
        """
        get_key = self.session.get(key)
        self.session.close()
        return get_key

    def keys(self) -> T:
        """
        获取所有键
        :return:
        """
        keys_all = self.session.keys()
        self.session.close()
        return keys_all

    @property
    def opt(self) -> T:
        """
        reis 操作   RedisPoolCluster.opt.xxxx
        :return:
        """
        return self.session
