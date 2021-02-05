# -*- coding: utf-8 -*-
# @File: common.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/2/1  16:11



from public.getcasedata import GetCaseData


class ErrorExcep(Exception):
    """
    自定义异常类
    """

    def __init__(self, message):
        super().__init__(message)


class Get:
    """
    获取测试数据
    """
    @staticmethod
    def test_data(yamlname, casename):
        testdata = GetCaseData(yamlname, casename).test_data_values()
        return testdata

