# -*- coding: utf-8 -*-
# @File: login.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/22  16:21

import os, sys

sys.path.append(os.pardir)

from public.logs import logger
from public.web_base import WebBase

yamlfile = os.path.basename(__file__).replace('py', 'yaml') #获取当前目运行文件 并替换为 yaml 后缀

'''

pageobj  对应 locatorYAML 操作页面
'''

class BaiDu(WebBase):


    def input_search_content(self,content):
        """
        输入搜索内容
        :param content: 输入内容
        :return:
        """
        # d = self.get_locator(yamlfile, 'input_search_content')
        # self.web_expression(types=d.types(0), locate=d.locate(0), operate=d.operate(0), text=content, notes='输入搜索内容')
        self.webexe(yamlfile, 'input_search_content',text=content)

    def click_search_button(self):
        """
        点击百度一下
        :return:
        """

        # d = self.get_locator(yamlfile, 'click_search_button')
        # self.web_expression(types=d.types(0), locate=d.locate(0), operate=d.operate(0),notes='点击百度一下')
        self.webexe(yamlfile, 'click_search_button')
