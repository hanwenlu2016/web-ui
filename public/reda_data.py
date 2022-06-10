# -*- coding: utf-8 -*-
# @File: getyaml.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/27  10:33

import os
import pickle
from typing import List, Tuple

import yaml
from faker import Factory
from xlrd import open_workbook

from config import CASEYMAL_DIR, LOCATORYMAL_DIR
from public.common import ErrorExcep, logger, reda_conf
from public.db import RedisPool

fake = Factory().create('zh_CN')



# 读取Excel 数据
class RedaExcel:
    """
    *xrld ==1.2.0
    读取excel文件中的内容。返回list。
    如：
    excel中内容为：
    | A  | B  | C  | x |
    | A1 | B1 | C1 | . |
    | A2 | B2 | C2 | . |

    默认输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    line=False输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """

    def __init__(self, excel: str, sheet: int or str = 0, line: bool = True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)

            if type(self.sheet) not in [int, str]:
                raise ErrorExcep('sheet类型错误')
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行为title
                for col in range(1, s.nrows):  # 依次遍历其余行，与首行组成dict，拼到self._data中
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):  # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data


# 读取yaml数据
class GetCaseYmal:
    """
    步骤数据 locatorYaml
     获取测试用例 locatorYaml数据类
    """

    def __init__(self, yaml_name: str, case_name: str = None) -> None:
        """
        :param yaml_name:  yaml 文件名称
        :param case_name:  用列名称 对应 yaml 用列
        """
        # 读取配置参数
        IS_REDIS= reda_conf('CURRENCY').get('IS_REDIS')
        self.isredis = IS_REDIS  # 是否读取reds数据

        self.yaml_name = yaml_name  # yaml 文件名称 拼接后的路径

        if case_name is not None:  # 如果用例名称不为空 可自动识别读取定位数据还是测试数据
            self.modelname = yaml_name  # 模块名称 对应yaml 文件名
            self.case_name = case_name  # 用列名称 对应 yaml 用列

            if case_name.startswith('test'):
                self.FLIE_PATH = os.path.join(CASEYMAL_DIR, f"{self.yaml_name}")
            else:
                self.FLIE_PATH = os.path.join(LOCATORYMAL_DIR, f"{self.yaml_name}")
        else:  # 没有用例名称 直接返回定位用例yaml路径
            self.FLIE_PATH = os.path.join(LOCATORYMAL_DIR, f"{self.yaml_name}")

    def open_yaml(self):
        """
        读取yaml文件
        :return: dict
        """
        try:
            with open(self.FLIE_PATH, encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                f.close()
                return data
        except UnicodeDecodeError:
            with open(self.FLIE_PATH, encoding='GBK') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                f.close()
                return data
        except  Exception:
            logger.error('Error opening ymal file')

    def get_yaml(self):
        """
        返回yaml文件数据
        :return: dict
        """
        yaml_data = self.open_yaml()
        if yaml_data is not None:
            return yaml_data[1:]  # 返回用列数据不包含 - model : login 部分 从列表1位置索引
        else:
            logger.error('The ymal file is empty')
            raise ('The ymal file is empty')

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

    def count_test_data(self):
        """
        统计 yaml  data 测试数据的条数
        :return:
        """
        yamlList = self.get_yaml()
        for yaml in yamlList:
            # 如果用列等于当前 用列就返回
            if yaml.get('casename') == self.case_name:
                try:
                    testdata_len = len(yaml.get('testdata'))

                    return testdata_len
                except  Exception as e:
                    logger.error(e)
                    pass

    def dataCount(self):
        """
        统计 data  数据条数
        :return:
        """
        if self.isredis:
            return self.redis_data_count()
        return self.count_test_data()

    def stepCount(self):
        """
        统计 yaml 测试步骤条数
        :return:
        """
        if self.isredis:
            dataList = self.redi_all()
        else:
            dataList = self.get_yaml()

        if dataList:
            for data in dataList:
                # 如果用列等于当前 用列就返回
                if data.get('casename') == self.case_name:
                    return len(data.get('element'))
        else:
            logger.error('用例不存在！请检查ymla文件')
            raise ErrorExcep('用例不存在！请检查文件')

    def get_param(self, value: str) -> str:
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

    def get_set(self, index: int, vaule: str):
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
                data = eval(redis.get('testdata'))
                return len(data)

        return "casename 不存在！"

    def redis_param(self, value: str) -> str:
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

    @property
    def get_model(self):
        """
        返回yaml
        :return: dict
        """
        data = self.open_yaml()
        return data[0].get('model')  #

    @property
    def title(self):
        """
        返回用列 title 标题
        :return: str
        """
        # 如果isredis Ture 就读取redis 参数值 否则读取yaml
        if self.isredis:
            return self.redis_param('title')
        return self.get_param('title')

    @property
    def precond(self):
        """
        返回用列 precond  前置条件
        :return: str
        """
        # 如果isredis Ture 就读取redis 参数值 否则读取yaml
        if self.isredis:
            return self.redis_param('precond')
        return self.get_param('precond')

    @property
    def reqtype(self):
        """
        ** HTTP 接口请求参数
        返回用列 reqtype  请类型
        :return: str
        """
        # 如果isredis Ture 就读取redis 参数值 否则读取yaml
        if self.isredis:
            return self.redis_param('reqtype')
        return self.get_param('reqtype')

    @property
    def header(self):
        """
        ** HTTP 接口请求参数
        返回用列 header  请求头
        :return: str
        """
        # 如果isredis Ture 就读取redis 参数值 否则读取yaml
        if self.isredis:
            return self.redis_param('header')
        return self.get_param('header')

    @property
    def urlpath(self):
        """
        ** HTTP 接口请求参数
        返回用列 urlpath  接口请求路径
        :return: str
        """
        # 如果isredis Ture 就读取redis 参数值 否则读取yaml
        if self.isredis:
            return self.redis_param('urlpath')
        return self.get_param('urlpath')

    def test_data_values(self, ):
        """
        读取yaml  测试数据的 values
        :return:  demo [('u1', 'p1', 'i1'), ('u2', 'p2', 'i2'), ('u3', 'p3', 'i3')]
        """

        data_values_list = []
        if self.isredis:
            dataList = self.redi_all()
        else:
            dataList = self.get_yaml()

        for data in dataList:
            # 如果用列等于当前 用列就返回 并且读取的是 yaml 数据

            if data.get('casename') == self.case_name and self.isredis == False:
                data_list = data.get('testdata')
                if data_list is not None:
                    for i in data_list:
                        data_values_list.append(tuple(i.values()))
                    return data_values_list
                else:
                    logger.info('没有测试数据')
                    continue

            elif data.get('casename') == self.case_name and self.isredis:
                # 读取是redis 时  data.get('data') 是字符串需要转为字典 列表
                data_list = eval(data.get('testdata'))
                if data_list is not None:
                    for i in data_list:
                        data_values_list.append(tuple(i.values()))
                    return data_values_list
                else:
                    logger.info('没有测试数据')
                    continue

    def test_data_list(self, index: int, agrs: str) -> str:
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
                    return data.get('testdata')[index].get(agrs)

                elif data.get('casename') == self.case_name and self.isredis:
                    # 读取是redis 时  data.get('data') 是字符串需要转为字典 列表
                    return eval(data.get('testdata'))[index].get(agrs)

        logger.error(f'{self.case_name}用列只有{self.dataCount()}条数据，你输入了第{index} 条！')

    def test_data(self):
        """
        返回yanl  testdat 全部数据 列表字段
        :return:
        """
        if self.isredis:
            return self.redi_all().get('testdata')
        return self.get_current_data().get('testdata')

    def casesteid(self, index: int) -> int:
        """
       返回 用列步骤 casesteid 参数
       """
        return self.get_set(index, 'casesteid')

    def types(self, index: int) -> str:
        """
        返回 用列步骤 types 参数
        """
        return self.get_set(index, 'types')

    def ios_types(self, index: int) -> str:
        """
        返回 用列步骤 ios_types 参数
        """
        return self.get_set(index, 'ios_types')

    def android_types(self, index: int) -> str:
        """
        返回 用列步骤 android_types 参数
        """
        return self.get_set(index, 'android_types')

    def operate(self, index: int) -> str:
        """
        返回 用列步骤 operate 参数
        """
        return self.get_set(index, 'operate')

    def ios_locate(self, index: int) -> str:
        """
        返回 用列步骤 ios_locate 参数
        """
        return self.get_set(index, 'ios_locate')

    def android_locate(self, index: int) -> str:
        """
        返回 用列步骤 android_locate 参数
        """
        return self.get_set(index, 'android_locate')

    def locate(self, index: int) -> str:
        """
        返回 用列步骤 locate 参数
        """
        return self.get_set(index, 'locate')

    def listindex(self, index: int) -> int:
        """
        返回 用列步骤 listindex 参数
        """
        return self.get_set(index, 'listindex')

    def locawait(self, index: int or float) -> int or float:
        """
        返回 用列步骤 locawait 参数
        """
        return self.get_set(index, 'locawait')

    def info(self, index: int) -> str:
        """
        返回 用列步骤 info 参数
        """
        return self.get_set(index, 'info')


# faker 随机数据类
class RandomData:
    """
    基于 faker 封装个人测试信息类
    """

    @property
    def random_name(self):
        """
        随机姓名
        :return: str
        """
        return fake.name()

    @property
    def random_phone_number(self):
        """
        随机手机号码
        :return:  int
        """
        return fake.phone_number()

    @property
    def random_email(self):
        """
        随机邮箱
        :return:
        """
        return fake.email()

    @property
    def random_job(self):
        """
       随机职位
       :return:
       """
        return fake.job()

    @property
    def random_ssn(self):
        """
       随机 省份证信息
       :return:
       """
        return fake.ssn(min_age=18, max_age=90)

    @property
    def random_company(self):
        """
        随机 公司名
        :return:
        """
        return fake.company()

    @property
    def random_city(self):
        """
        随机 城市
        :return:  str
        """
        return fake.city_name()

    @property
    def random_province(self):
        """
        随机 省份
        :return:  str
        """
        return fake.province()

    @property
    def random_country(self):
        """
        随机 国家
        :return:  str
        """
        return fake.country()

    @property
    def random_address(self):
        """
        随机住址信息
        :return:  str
        """
        return fake.address()

    @property
    def random_time(self):
        """
        随机时间24H   22:00:00
        :return: str
        """
        return fake.time()

    @property
    def random_year(self):
        """
        随机月份
        :return: str[0] -数字月  str[0] -英文月
        """
        return (fake.month(), fake.month_name())

    @property
    def random_month(self):
        """
        随机年份
        :return: str
        """
        return fake.month()

    @property
    def random_date_this_month(self):
        """
        随机 本月中的日期时间
        :return: str
        """
        return fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)

    @property
    def random_date_this_decade(self):
        """
        随机 本年中的日期时间
        :return: str
        """
        return fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)

    @property
    def random_date_time_this_century(self):
        """
        随机 本世纪中的日期和时间
        :return: str
        """
        return fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)

    @property
    def random_day_of_week(self):
        """
        随机星期
        :return:  str
        """
        return fake.day_of_week()

    def random_date_of_birth(self, age):
        """
        随机生日
        :param age:  int  需要随机多少岁之内
        :return:  str
        """
        return fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=age)


def replace_py_yaml(file):
    """
    当前py文件转为 yaml后缀
    :param file:
    :return:
    """
    return os.path.basename(file).replace('py', 'yaml')





# 快速获取测试数据 *元组 WEB、APP
def reda_pytestdata(yamlname: str, casename: str, ) -> List or Tuple:
    """
    * pytest.mark.parametrize()  *此函数只支持在pytes框架内使用
    * 如果配合run函数调用自己在pytest.mark.parametrize() 传入列表 否则其它方法传入字段名
    快速获取测试数据 *元组
    :param yamlname: yaml 名称
    :param casename:   用例数据
    :return:
    """
    yaml = replace_py_yaml(yamlname)
    testdata = GetCaseYmal(yaml, casename).test_data_values()
    return testdata


#  快速获取测试数据 *字典 API
def reda_api_casedata(yamlname: str, casename: str) -> List or Tuple:
    """
    读取测试数据 HTTP 专用  *字典
    :return:
    """
    yaml = replace_py_yaml(yamlname)
    testdata = GetCaseYmal(yaml, casename)

    return testdata.test_data()


# 写入到yaml文件
if __name__ == '__main__':
    # IS_CLEAN_REPORT=reda_seting_yaml()[0].get('IS_CLEAN_REPORT')
    # print(reda_seting_yaml()[0].get('CURRENCY').get('IS_CLEAN_REPORT'))
    # print(reda_seting_yaml())

    print(reda_conf('CURRENCY').get('IS_CLEAN_REPORT'))
