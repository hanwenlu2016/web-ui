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


class WangYi(WebBase):


    def froms(self):    # 如果需要跳转回来 使用switch_default_content
        """
        跳转iffrom
        :return:
        """
        self.webexe(yamlfile, 'froms')

    def input_user(self,user):
        """
        输入用户
        :return:
        """

        self.webexe(yamlfile, 'input_user',text=user)

    def input_pwd(self,pwd):
        """
        输入密码
        :return:
        """
        self.webexe(yamlfile, 'input_pwd',text=pwd)

    def input_sub(self):
        """
        提交登录
        :return:
        """
        self.webexe(yamlfile, 'input_sub')

