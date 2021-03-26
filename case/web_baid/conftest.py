# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest
from pyvirtualdisplay import Display

from public.driver_init import WebInit,if_linux_firefox



# luinx 服务器时需要特殊处理
@pytest.fixture(scope='session', autouse=True)
def webDriver():
    display = Display(visible=0, size=(800, 600))

    if if_linux_firefox:
        yield display.start()
        display.stop()


@pytest.fixture(scope='function', autouse=True)
def webDriver():
    wb = WebInit()
    driver = wb.enable
    yield driver
    driver.quit()

# @pytest.fixture(scope='function', autouse=True)
# def webDriver():
#     wb = WebInit()
#     driver = wb.enable
#
#     if wb.if_linux_firefox():  # 如果是  linux系统并且是firefox 浏览器需要特殊处理
#         yield driver[0]
#         driver[0].quit()
#         driver[1].stop()
#     else:
#         yield driver
#         driver.quit()
