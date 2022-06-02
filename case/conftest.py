# -*- coding: utf-8 -*-
# @File: conftest.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  20:16

import pytest

from public.driver_init import WebInit, AppInit
from config.setting import CASE_TYPE


@pytest.fixture(scope='function')
def goDriver():
    if CASE_TYPE.lower() == 'app':
        driver = AppInit().setup()
        yield driver
        driver.quit()
    else:
        driver = WebInit().enable
        yield driver
        driver.quit()

