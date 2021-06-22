# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest

from public.driver_init import WebInit,AppInit



# luinx 服务器时需要特殊处理
#@pytest.fixture(scope='session', autouse=True)
# def webDriver():
#     display = Display(visible=0, size=(800, 600))
#
#     if if_linux_firefox:
#         yield display.start()
#         display.stop()


@pytest.fixture(scope='function')
def webDriver():
    wb = WebInit()
    driver = wb.enable
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def appDriver():
    driver = AppInit().setup()
    yield driver
    driver.quit()

