# -*- coding: utf-8 -*-
# @File: android.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/22  12:57

import os, sys

sys.path.append(os.pardir)

from public.app_base import AppBase

yamlfile = os.path.basename(__file__).replace('py', 'yaml')


class OpenWeChatPage(AppBase):

    def click_login_button(self,):

        self.appexe(yamlfile, 'click_login_button',)
