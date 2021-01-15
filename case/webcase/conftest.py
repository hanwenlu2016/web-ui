# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest

from public.web.webdriverfactory import WebBrowserDriver


@pytest.fixture(scope='function', autouse=True)
def webDriver():
    driver = WebBrowserDriver.opt()

    yield driver

    driver.close()
    driver.quit()
