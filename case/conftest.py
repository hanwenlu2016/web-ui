# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest

from public.driver_init import WebInit, AppInit


@pytest.fixture(scope='function')
def webDriver():
    driver = WebInit().enable
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def appDriver():
    driver = AppInit().setup()
    yield driver
    driver.quit()
