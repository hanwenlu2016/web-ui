# -*- coding: utf-8 -*-
# @File: test_app_demo.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/13  19:21

import time

import pytest
import allure
from selenium.webdriver.common.by import By
from public.logs import logger
from pageobj.appobj.jd import Jd


class TestJd:

    @allure.feature("打开京东点击我的")
    @allure.title("启动验证")
    @pytest.mark.jd
    def test_openJD(self, appDriver):
        with allure.step('打开京东点击我的'):

            Jd(appDriver).openjd()




