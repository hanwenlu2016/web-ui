# -*- coding: utf-8 -*-
# @File: getyaml.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/27  10:33


import os
import pickle

import yaml

from public.logs import logger
from public.db import RedisPool
from config.setting import DATA_YAML, IS_REDIS


class GetCaseData:
    """
     获取测试用例 Yaml数据类
    """

    def __init__(self, yaml_name, case_name):
        """
        :param yaml_name:  yaml 文件名称
        :param case_name:  用列名称 对应 yaml 用列
        """
        self.isredis = IS_REDIS  # 是否读取reds数据
        self.modelname = yaml_name  # 模块名称 对应yaml 文件名

        self.yaml_name = yaml_name  # yaml 文件名称 拼接后的路径
        self.case_name = case_name  # 用列名称 对应 yaml 用列

        self.FLIE_PATH = os.path.join(DATA_YAML, f"{self.yaml_name}")

        try:
            if os.path.exists(self.FLIE_PATH):
                self.yaml_name = self.FLIE_PATH
            else:
                logger.info("文件不存在")
            self._all_data = None
        except Exception as e:
            logger.error(e)

    def open_yaml(self):
        """
        读取yaml文件
        :return: dict
        """

        try:
            with open(self.FLIE_PATH) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                f.close()
                return data
        except Exception as e:
            logger.error(e)
            logger.error(f'读取yaml失败！{e}')

    def get_yaml(self):
        """
        返回yaml文件数据
        :return: dict
        """
        data = self.open_yaml()
        return data[1:]  # 返回用列数据不包含 - model : login 部分 从列表1位置索引

    def get_current_data(self):
        """
        返回 yaml 当前用列的所有数据
        :return: dict
        """
        yamlList = self.get_yaml()
        for yaml in yamlList:
            # 如果用列等于当前 用列就返回
            if yaml.get('casename') == self.case_name:
                return yaml
        return "casename 不存在！"

    def count_data(self):
        """
        统计 yaml  data 测试数据的条数
        :return:
        """
        yamlList = self.get_yaml()
        for yaml in yamlList:
            # 如果用列等于当前 用列就返回
            if yaml.get('casename') == self.case_name:
                return len(yaml.get('data'))
        return "casename 不存在！"

    def dataCount(self):
        """
        统计 data  数据条数
        :return:
        """
        if self.isredis:
            return self.redis_data_count()
        return self.count_data()

    def stepCount(self):
        """
        统计 yaml 测试步骤条数
        :return:
        """
        if self.isredis:
            dataList = self.redi_all()
        else:
            dataList = self.get_yaml()

        for data in dataList:
            # 如果用列等于当前 用列就返回
            if data.get('casename') == self.case_name:
                return len(data.get('element'))
        return "casename 不存在！"

    def get_param(self, value):
        """
        获取 yaml用列参数
        :param value:  传递参数值
        :return:
        """

        yamlList = self.get_yaml()
        for yaml in yamlList:
            # 如果用列等于当前 用列就返回
            if yaml.get('casename') == self.case_name:
                return yaml.get(value)
        return "casename 不存在！"

    def get_set_data(self, index, vaule):
        """
        获取 set 用列步骤数据

        :param index: 列表索引位置
        :param vaule:  参数值
        :return:
        """
        # 如果读取redis 就从redis获取数据 否则从yaml获取

        if self.isredis:
            dataList = self.redi_all()
        else:
            dataList = self.get_yaml()
        if index < self.stepCount():
            for data in dataList:
                # 如果用列等于当前 用列就返回
                if data.get('casename') == self.case_name:
                    return data.get('element')[index].get(vaule)
        logger.error(f'{self.case_name}用列只有{self.stepCount()}个步骤，你确输入了{index} 步！')
        return None

    def redi_all(self):
        """
        redis 返回全部数据
        :return:
        """

        try:
            re = RedisPool()
            modellanme = self.modelname.replace('.yaml', '')  # modellanme 模块  redis 不读.yaml 后缀
            unpacked_object = pickle.loads(re.session.get(modellanme))
            return unpacked_object
        except TypeError as e:

            logger.error(e)

    def redi_case(self):
        """
        redis 返回redis 指定用列数据
        :return:
        """
        data = self.redi_all()
        for da in data:
            # 如果用列等于当前 用列就返回
            if da.get('casename') == self.case_name:
                return da
        return "casename 不存在！"

        # return unpacked_objectK

    def redis_data_count(self, ):
        """
       统计 rededis  data 测试数据的条数
       :return:
       """
        redisList = self.redi_all()
        for redis in redisList:
            if redis.get('casename') == self.case_name:
                # redis data数据是字符串 转为字典列表
                data = eval(redis.get('data'))
                return len(data)

        return "casename 不存在！"

    def redis_param(self, value):
        """
        获取 redis用列参数
        :param value:  传递参数值
        :return:
        """
        redisList = self.redi_all()
        for redis in redisList:

            if redis.get('casename') == self.case_name:
                return redis.get(value)
        return "casename 不存在！"

    def get_model(self):
        """
        返回yaml
        :return: dict
        """
        data = self.open_yaml()
        return data[0].get('model')  #

    def title(self):
        """
        返回用列 title 标题
        :return: str
        """
        # 如果isredis Ture 就读取redis 参数值 否则读取yaml
        if self.isredis:
            return self.redis_param('title')
        return self.get_param('title')

    def precond(self):
        """
        返回用列 precond  前置条件
        :return: str
        """
        # 如果isredis Ture 就读取redis 参数值 否则读取yaml
        if self.isredis:
            return self.redis_param('precond')
        return self.get_param('precond')

    def data(self, index, agrs):
        """
        返回 用列 测试 data 数据列表
        :param index: 列表的索引位置
        :param agrs: 字段的key  因为测试数据是可变的增加的
        :return:
        """
        if self.isredis:
            dataList = self.redi_all()
        else:
            dataList = self.get_yaml()

        if index < self.dataCount():

            for data in dataList:
                # 如果用列等于当前 用列就返回 并且读取的是 yaml 数据

                if data.get('casename') == self.case_name and self.isredis == False:
                    return data.get('data')[index].get(agrs)

                elif data.get('casename') == self.case_name and self.isredis == True:
                    # 读取是redis 时  data.get('data') 是字符串需要转为字典 列表
                    return eval(data.get('data'))[index].get(agrs)

        logger.error(f'{self.case_name}用列只有{self.dataCount()}条数据，你输入了第{index} 条！')
        # return None

    def casesteid(self, index):
        """
       返回 用列步骤 casesteid 参数
       """
        return self.get_set_data(index, 'casesteid')

    def types(self, index):
        """
        返回 用列步骤 types 参数
        """
        return self.get_set_data(index, 'types')

    def operate(self, index, ):
        """
        返回 用列步骤 operate 参数
        """
        return self.get_set_data(index, 'operate')

    def locate(self, index):
        """
        返回 用列步骤 operate 参数
        """
        return self.get_set_data(index, 'locate')

    def info(self, index):
        """
        返回 用列步骤 info 参数
        """
        return self.get_set_data(index, 'info')

    def expect(self, index):
        """
        返回 用列步骤 expect 参数
        """
        return self.get_set_data(index, 'expect')


