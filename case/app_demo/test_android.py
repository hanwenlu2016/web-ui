# -*- coding: utf-8 -*-
# @File: test_android.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/22  16:58

# -*- coding: utf-8 -*-
# @File: test_android.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/22  11:43

import os

import allure
import pytest

from pageobj.android import OpenWeChatPage



class TestAndroidDemo:

    @allure.feature("打开微信")  # 测试用例特性（主要功能模块）
    @allure.story("打开微信")  # 模块说明
    @allure.title("打开微信")  # 用例标题
    @allure.description('打开微信')  # 用例描述
    @pytest.mark.test_open_wechat_addroid
    def test_open_wechat(self, goDriver):
        with allure.step('打开微信'):
            op = OpenWeChatPage(goDriver)
            op.click_login_button()
            op.sleep(3)
