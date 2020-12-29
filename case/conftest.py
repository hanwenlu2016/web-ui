# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest
from public.webdriverfactory import WebBrowserDriver


@pytest.fixture(scope='session', autouse=True)
def one_browser():

    driver = WebBrowserDriver.opt()

    yield driver

    driver.close()
    driver.quit()
