# -*- coding: utf-8 -*-
# @File: run.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  19:04

import  os ,sys

sys.path.append(os.pardir)

import pytest
from config.setting import *
from public.logs import logger
from public.cleanup import del_clean_report


def run():
    """
    运行所有测试用例
    :return: noul
    """

    # 执行前检查是否清除报告
    del_clean_report()


    # 执行用列
    #pytest.main(['-s', '-v', '-m','test_login_and_out', '-n=1','--reruns=1', '--alluredir', f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])
    pytest.main(['-s', '-v',  '-n=1','--reruns=0', '--alluredir', f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])
    '''
   -m 代表 运行指定模块
   -n 代表 几个线程
   --reruns 代表失败重跑次数
   '''


    # 生成测试报告
    os.system(f'allure generate {PRPORE_JSON_DIR} -o {PRPORE_ALLURE_DIR} --clean')

    logger.info('测试报告生成完成！')


if __name__ == '__main__':
    run()
