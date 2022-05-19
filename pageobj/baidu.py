# -*- coding: utf-8 -*-
# @File: login.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/22  16:21

import os
import sys

sys.path.append(os.pardir)

from public.web_base import WebBase

yamlfile = os.path.basename(__file__).replace('py', 'yaml')  # 获取当前目运行文件 并替换为 yaml 后缀

'''

pageobj  对应 locatorYAML 操作页面
'''


class BaiDu(WebBase):

    def input_search_content(self, content):
        """
        输入搜索内容
        :param content: 输入内容
        :return:
        """

        self.webexe(yamlfile, 'input_search_content', text=content)

    def click_search_button(self):
        """
        点击百度一下
        :return:
        """

        self.webexe(yamlfile, 'click_search_button')

