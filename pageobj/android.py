# -*- coding: utf-8 -*-
# @File: android.py.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/22  12:57

import os
import sys

sys.path.append(os.pardir)

from public.app_base import AppBase




class OpenWeChatPage(AppBase):

    def click_login_button(self, ):
        self.appexe(__file__, sys._getframe().f_code.co_name )
