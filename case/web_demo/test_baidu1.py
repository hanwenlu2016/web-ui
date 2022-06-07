# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  11:08

import os

import allure
import pytest

from public.reda_data import reda_pytestdata
from public.web_base import AutoRunCase


# 修改 setting  URL
class TestBaiDu:

    @allure.feature("百度搜索")  # 测试用例特性（主要功能模块）
    @allure.story("所搜验证")  # 模块说明
    @allure.title("输入内容并搜索")  # 用例标题
    @allure.description('输入多参数搜索')  # 用例描述
    @pytest.mark.testbaidu_web1  # 用列标记
    @pytest.mark.parametrize('testdate', reda_pytestdata(__file__, 'test_baidu_search'))  # 测试数据
    def test_baidu_search(self, goDriver, testdate):
        with allure.step('输入搜索内容'):
            baidu = AutoRunCase(goDriver)

            baidu.run(__file__, 'test_baidu_search', test_date=testdate, forwait=1)
