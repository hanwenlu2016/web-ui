# -*- coding: utf-8 -*-
# @File: run.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  19:04

import os, sys

sys.path.append(os.pardir)

import pytest
from config.ptahconf import *
from public.logs import logger
from public.common import del_clean_report
from public.common import value_division


def run_modle(m, n, reruns, mlist, dir):
    """
    判断运行模块
    :param m:  模块
    :param n: 线程数
    :param reruns:  失败重跑次数
    :param mlist:  多模块列表
    :param dir: 结果目录
    :return:
    """
    var = value_division(mlist)
    JSON_DIR = dir

    if m == 'all':  # all 运行所有模块用例
        logger.info('运行当前项目所有用例开始！！！')
        pytest.main(['-s', '-v', f'-n={n}', f'--reruns={reruns}', '--alluredir', f'{JSON_DIR}', f'{CASE_DIR}'])

    elif ',' not in m and m != 'all':  # 传递1个模块时执行
        logger.info(f'运行当前项目模块用例{m}开始！！！')
        pytest.main(['-s', '-v', '-m', f'{m}', f'-n={n}', f'--reruns={reruns}', '--alluredir', f'{JSON_DIR}',
                     f'{CASE_DIR}'])

    elif ',' in m and len(mlist) <= 5:  # 传递2个模块时执行
        logger.info(f'运行当前项目模块用例{mlist}开始！！！')
        pytest.main(
            ['-s', '-v', '-m', f'{var}', f'-n={n}', f'--reruns={reruns}', '--alluredir', f'{JSON_DIR}',
             f'{CASE_DIR}'])

    else:  # 运行传递模块用例
        logger.info(f'传递参数错误！！')


def output_path(dir):
    """
    生成测试报告路径
    :param dir: 目录
    :return:
    """
    # 测试用例结果目录
    PRPORE_JSON_DIR = os.path.join(BASE_DIR, "output", "{}".format(dir), "report_json")

    # 测试结果报告目录
    PRPORE_ALLURE_DIR = os.path.join(BASE_DIR, "output", "{}".format(dir), "report_allure")

    # 测试截图目录
    PRPORE_SCREEN_DIR = os.path.join(BASE_DIR, "output", "{}".format(dir), "report_screen")

    # 判断路径文件是否存在 不存在就创建
    listpathdir = [PRPORE_JSON_DIR, PRPORE_ALLURE_DIR, PRPORE_SCREEN_DIR]
    for pathdir in listpathdir:
        if not os.path.exists(pathdir):
            os.makedirs(pathdir)

    return PRPORE_JSON_DIR, PRPORE_ALLURE_DIR, PRPORE_SCREEN_DIR


def run():
    """
    运行所有脚本
    :return: noul
    """

    # 执行前检查是否清除报告
    del_clean_report()

    # 模块名称
    m = sys.argv[1]  # 1模块名称 Python run.py all 1 1   、 Python run.py test1,test2,test3 3 1
    mlist = None

    if ',' in m:
        mlist = m.split(',')

    n = sys.argv[2]  # 2线程数据
    reruns = sys.argv[3]  # 3失败重跑次数
    dir = sys.argv[4]  # 4生成结果目录

    if int(n) <= 0 or int(n) is None:
        n = 1

    if int(reruns) <= 0 or int(reruns) is None:
        reruns = 1

    # 生成测试结果目录
    outpath = output_path(dir)

    # 运行模块
    run_modle(m, n, reruns, mlist, outpath[0])

    os.system(f'allure generate {outpath[0]} -o {outpath[1]} --clean')
    logger.info('测试报告生成完成！')
    dd = os.path.join(outpath[0], 'index.html')
    logger.info(dd)
    return dd


def run_bebug():
    # 执行前检查是否清除报告
    #del_clean_report()
    pytest.main(['-s', '-v', '-n=1', '--reruns=0', '-W','ignore:Module already imported:pytest.PytestWarning','--alluredir', f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])
    # os.system(f'allure generate {PRPORE_JSON_DIR} -o {PRPORE_ALLURE_DIR} --clean')
    # logger.info('测试报告生成完成！')


if __name__ == '__main__':
    #run()
    run_bebug()
# Python run.py all(项目或者模块) 1(线程数) 1(失败重跑次数) dir(生成目录名称)





'''
    -m 代表 运行指定模块 all
    -n 代表 几个线程
    --reruns 代表失败重跑次数
'''

# 执行用列
# parameter_set()
# pytest.main(['-s', '-v', '-n=0', '--reruns=0', '--alluredir', f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])
# pytest.main(['-s', '-v', '-m', 'test_cc ', f'-n=1', f'--reruns=1', '--alluredir', f'{PRPORE_JSON_DIR}',f'{CASE_DIR}'])
# pytest.main(['-s', '-v', '-m', 'test_cc ', f'-n=1', f'--reruns=1', '--alluredir', f'{outpath[0]}', f'{CASE_DIR}'])

# 生成测试报告
# os.system(f'allure generate {PRPORE_JSON_DIR} -o {PRPORE_ALLURE_DIR} --clean')
