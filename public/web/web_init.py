# -*- coding: utf-8 -*-
# @File: webdriverfactory.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/28  10:49

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.web_setting import CHROMEDRIVER, FIREFOXDRIVER, IEDRIVER
from config.web_setting import BROWSERNAME, URL
from public.logs import logger


class WebBrowserDriver:
    """
    返回浏览器驱动
    """
    browser = BROWSERNAME.lower()
    baseurl = URL

    @classmethod
    def opt(cls):
        """
        获取浏览器
        :return:
        """

        global driver
        try:
            if cls.browser == 'chrome':
                driver = webdriver.Chrome(executable_path=CHROMEDRIVER)

            elif cls.browser == 'firefox':
                driver = webdriver.Firefox(executable_path=FIREFOXDRIVER)

            elif cls.browser == 'ie':
                driver = webdriver.Ie(executable_path=IEDRIVER)
            else:
                logger.info('不支持此浏览器')
                return '不支持此浏览器！'

            driver.maximize_window()
            driver.get(cls.baseurl)
            logger.info(f'启动{cls.browser}浏览器')
            return driver
        except Exception as e:
            logger.error(f'浏览器驱动启动失败 {e}')



