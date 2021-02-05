# -*- coding: utf-8 -*-
# @File: login.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/22  16:21

from public.logs import logger
from public.getcasedata import GetCaseData
from public.web.webbase import WebBase


'''

所有页面操作可在 pageobj 文件下 创建自己的业务逻辑定位
'''

class Baidu(WebBase): # 对应 test_baidu.py 业务逻辑

    def index(self):
        """
        登录操作
        :return:
        """
        lo = GetCaseData('baidu.yaml', 'test_index')

        self.used_input(text=lo.data(0, 'vue1'), types=lo.types(0), locate=lo.locate(0))

        self.used_click(types=lo.types(1),locate= lo.locate(1))

    def home(self):
        pass