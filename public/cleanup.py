# -*- coding: utf-8 -*-
# @File: clean_up.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/11/3  17:48

import os
import shutil

from config.setting import PRPORE_ALLURE_DIR, PRPORE_JSON_DIR, PRPORE_SCREEN_DIR, IS_CLEAN_REPORT


def clean_report(filepath):
    """
    清除测试报告文件
    :param filepath:  str  清除路径
    :return:
    """
    del_list = os.listdir(filepath)

    for f in del_list:
        file_path = os.path.join(filepath, f)

        # 判断是不是文件
        if os.path.isfile(file_path):
            if not file_path.endswith('.xml'):  # 不删除.xml文件
                os.remove(file_path)
        else:
            os.path.isdir(file_path)
            shutil.rmtree(file_path)


def del_clean_report():
    """
    执行删除测试报告记录
    :return:
    """
    if IS_CLEAN_REPORT == True: # 如果为 True 清除 PRPORE_ALLURE_DIR、 PRPORE_JSON_DIR 、PRPORE_SCREEN_DIR 路径下报告

        dir_list = [PRPORE_ALLURE_DIR, PRPORE_JSON_DIR, PRPORE_SCREEN_DIR]

        for dir in dir_list:
            clean_report(dir)

