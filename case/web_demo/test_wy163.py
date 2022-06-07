# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  11:08

import os

import allure
import pytest

from pageobj.wy163 import WangYi
from public import reda_pytestdata



# 修改 setting  URL
class TestWangYi:

    @allure.feature("网易登录")  # 测试用例特性（主要功能模块）
    @allure.story("测试iffrom")  # 模块说明
    @allure.title("测试iffrom")  # 用例标题
    @allure.description('测试iffrom')  # 用例描述
    @pytest.mark.testwy_web  # 用列标记
    @pytest.mark.parametrize('user,pwd', reda_pytestdata(__file__, 'test_wy63_go'))  # 测试数据
    def test_wy63_go(self, goDriver,user,pwd):
        wy = WangYi(goDriver)

        with allure.step('跳转iffrom'):
            wy.froms()
            wy.sleep(3)

        with allure.step('输入用户'):
            wy.input_user(user)
            wy.sleep(1)

        with allure.step('输入密码'):
            wy.input_pwd(pwd)
            wy.sleep(1)

        with allure.step('登录'):
            wy.input_sub()
            wy.sleep(5)

