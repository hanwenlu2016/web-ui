# -*- coding: utf-8 -*-
# @File: clean_up.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/11/3  17:48

import os
import shutil



def clean_report(filepath):
    """
    清除测试报告文件
    :param filepath:  str  清除路径
    :return:
    """
    del_list = os.listdir(filepath)

    for f in del_list:
        file_path = os.path.join(filepath, f)

        if os.path.isfile(file_path):
            if not file_path.endswith('.xml'):  # 不删除.xml文件
                os.remove(file_path)

        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

