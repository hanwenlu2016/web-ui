# -*- coding: utf-8 -*-
# @File: test_demo.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  11:08


import allure
import pytest
from public.logs import logger
from pageobj.baidu import Baidu

'''
case  文件下创建对应 pageobj 业务逻辑用列
'''
class TestBaidu:

    @allure.feature("打开百度搜索")
    @allure.title("打开百度搜索")
    # @pytest.mark.index
    def test_index(self, one_browser):
        """
        登录用列
        :param one_browser:
        :return:
        """
        with allure.step('登录用户'):
            logger.info('test_login')
            Baidu(one_browser).index()

    def test_hone(self, one_browser):
        pass
