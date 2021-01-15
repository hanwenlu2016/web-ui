# -*- coding: utf-8 -*-
# @File: appium_init.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/13  19:17

from appium import webdriver

from public.logs import logger
from config.app_setting import CAPABILITIES, APIUMHOST, APIUMPORT


class AppiumInit:
    """
    初始化APP连接信息类
    """

    @staticmethod
    def setup():
        try:
            caps = CAPABILITIES
            webdrivers = webdriver.Remote("http://" + APIUMHOST + ":" + APIUMPORT + "/wd/hub", caps)
            #webdrivers.implicitly_wait(10)

            return webdrivers
        except Exception as e:
            logger.error(f'初始app失败 {e}')


