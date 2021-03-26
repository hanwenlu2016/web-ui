# -*- coding: utf-8 -*-
# @File: conftest.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/3/26  15:11

import pytest
from public.driver_init import AppInit

# function class module session
@pytest.fixture(scope='session', autouse=True)
def appDriver():

    driver = AppInit().setup()
    yield driver

    driver.quit()