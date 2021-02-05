# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest
from public.app.app_init import AppiumInit

# function class module session
@pytest.fixture(scope='function', autouse=True)
def appDriver():

    driver = AppiumInit.setup()

    yield driver

    driver.quit()
