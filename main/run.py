# -*- coding: utf-8 -*-
# @File: run.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  19:04

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
    #pytest.main(['-s', '-v', '-m', 'me', '-n=1', '--alluredir', f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])
    pytest.main(['-s', '-v',  '-n=1', '--alluredir', f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])

    # 生成测试报告
    os.system(f'allure generate {PRPORE_JSON_DIR} -o {PRPORE_ALLURE_DIR} --clean')

    logger.info('测试报告生成完成！')


if __name__ == '__main__':
    run()
