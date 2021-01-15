# -*- coding: utf-8 -*-
# @File: login.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/22  16:21

from public.logs import logger
from public.getcasedata import GetCaseData
from public.web.webbase import Base


'''

所有页面操作可在 pageobj 文件下 创建自己的业务逻辑定位
'''

class Baidu(Base): # 对应 test_baidu.py 业务逻辑

    def index(self):
        """
        登录操作
        :return:
        """
        lo = GetCaseData('baidu.yaml', 'test_index')

        self.input_keys(lo.data(0, 'vue1'), lo.types(0), lo.locate(0))

        self.clicks(lo.types(1), lo.locate(1))

    def home(self):
        pass