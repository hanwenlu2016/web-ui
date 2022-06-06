# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest

from public.driver_init import WebInit, AppInit
from config.setting import CASE_TYPE, IS_EXIT_APPLICATION, PLATFORM, ANDROID_CAPA, IOS_CAPA


@pytest.fixture(scope='function')
def goDriver():
    if CASE_TYPE.lower() == 'app':
        driver = AppInit().enable
        yield driver

        if IS_EXIT_APPLICATION:  # 是否退出应用操作
            if PLATFORM.lower() == 'android':
                appname = ANDROID_CAPA["appPackage"]
            else:
                appname = IOS_CAPA["udid"]
            driver.terminate_app(appname)  # 退出应用
        driver.quit()
    else:
        driver = WebInit().enable
        yield driver
        driver.quit()
