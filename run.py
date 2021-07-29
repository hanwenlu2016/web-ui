# -*- coding: utf-8 -*-
# @File: run.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  19:04

import os, sys

sys.path.append(os.pardir)

from typing import List

import pytest

from config.ptahconf import *
from public.common import DelReport, ErrorExcep,logger


OUT_TITLE = """
══════════════════════════════════════════
║            WEB-UI-AUTO                 ║
║       No one can put out the stars !   ║
══════════════════════════════════════════
"""

logger.info(OUT_TITLE)



class RunPytest:

    @classmethod
    def value_division(cls, mlist: List) -> str:
        """
        参数值划分  生成demo '{} or {} or {}  '.format(mlist[0], mlist[1], mlist[2]) 根据传递长度生成 {} or
        """
        if mlist is not None:
            mdata = ''
            for index, i in enumerate(mlist):
                mdata += str(i)
                if index < len(mlist) - 1:
                    mdata += ' or '
            return mdata

    @classmethod
    def run_modle(cls, m, n, reruns, mlist, dir):
        """
        判断运行模块
        :param m:  模块
        :param n: 线程数
        :param reruns:  失败重跑次数
        :param mlist:  多模块列表
        :param dir: 生成结果项目目录名称
        :return:
        """
        var = cls.value_division(mlist)
        JSON_DIR = dir
        if m == 'all':  # all 运行所有模块用例
            logger.info('运行当前项目所有用例开始！！！')
            pytest.main(
                [f'-n={n}', f'--reruns={reruns}', '--alluredir', f'{JSON_DIR}', f'{CASE_DIR}'])
            return True

        elif ',' not in m and m != 'all' and m.startswith('test'):  # 传递1个模块时执行
            logger.info(f'运行当前项目模块用例{m}开始！！！')
            pytest.main(['-m', f'{m}', f'-n={n}', f'--reruns={reruns}', '--alluredir', f'{JSON_DIR}', f'{CASE_DIR}'])
            return True

        elif ',' in m and len(mlist) <= 5:  # 传递2个模块时执行
            logger.info(f'运行当前项目模块用例{mlist}开始！！！')
            pytest.main(
                ['-m', f'{var}', f'-n={n}', f'--reruns={reruns}', '--alluredir', f'{JSON_DIR}', f'{CASE_DIR}'])
            return True

        else:  # 运行传递模块用例
            logger.info(f'模块名称错误！！！')
            return False

    @classmethod
    def output_path(cls, dir):
        """
        生成测试报告路径
        :param dir: 目录名称
        :return:
        """
        # 测试用例结果目录
        PRPORE_JSON_DIR = os.path.join(BASE_DIR, "output", "{}".format(dir), "report_json")

        # 测试结果报告目录
        PRPORE_ALLURE_DIR = os.path.join(BASE_DIR, "output", "{}".format(dir), "report_allure")

        # 测试截图目录 暂时不生成零时图片目录
        # PRPORE_SCREEN_DIR = os.path.join(BASE_DIR, "output", "{}".format(dir), "report_screen")

        # 判断路径文件是否存在 不存在就创建
        listpathdir = [PRPORE_JSON_DIR, PRPORE_ALLURE_DIR]  # PRPORE_SCREEN_DIR
        for pathdir in listpathdir:
            if not os.path.exists(pathdir):
                os.makedirs(pathdir)

        return PRPORE_JSON_DIR, PRPORE_ALLURE_DIR

    @classmethod
    def receiving_argv(cls):
        """
        接收系统输入参数   1模块名称 2线程数据 3失败重跑次数 4生成结果目录名称  Python run.py all 1 1 demo
        :return:
        """
        # 1模块名称
        try:
            module_name = sys.argv[1]
            mlist = None
            if ',' in module_name:
                mlist = module_name.split(',')

            # 2线程数据
            thread_num = sys.argv[2]

            # 3失败重跑次数
            reruns = sys.argv[3]

            # 4 生成结果目录名称
            results_dir = sys.argv[4]

            if int(thread_num) <= 0 or int(thread_num) is None:
                thread_num = 1
            if int(reruns) <= 0 or int(reruns) is None:
                reruns = 1
            return results_dir, module_name, mlist, thread_num, reruns
        except Exception as e:
            logger.error(e)
            raise ErrorExcep('输入参数错误！')

    @classmethod
    def run(cls):
        """
        正式运行所有脚本 配置django 管理
        :return:
        """

        # 执行前检查是否清除报告
        DelReport().run_del_report()

        # 接收参数
        results_dir, module_name, mlist, thread_num, reruns = cls.receiving_argv()

        # 生成测试结果目录
        prpore_json_dir, prpore_allure_dir = cls.output_path(results_dir)

        # 判断运行模块
        run_modle = cls.run_modle(module_name, thread_num, reruns, mlist, prpore_json_dir)

        # 生成测试报告
        if run_modle:
            os.system(f'allure generate {prpore_json_dir} -o {prpore_allure_dir} --clean')
            logger.info('测试报告生成完成！')

            html_index = os.path.join(prpore_allure_dir, 'index.html')
            logger.info(html_index)
            return html_index

    @staticmethod
    def run_bebug():
        """
        bebug 调试
        :return:
        """

        # 执行前检查是否清除报告
        DelReport().run_del_report()

        pytest.main(
            ['-m', 'testbaidu_web','-n=1','--reruns=0', '--alluredir',f'{PRPORE_JSON_DIR}', f'{CASE_DIR}'])

        # os.system(f'allure generate {PRPORE_JSON_DIR} -o {PRPORE_ALLURE_DIR} --clean')
        # logger.info('测试报告生成完成！')




if __name__ == '__main__':

    #RunPytest.run()
    RunPytest.run_bebug()

# Python run.py all(项目或者模块) 1(线程数) 1(失败重跑次数) dir(生成目录名称)
# addopts 参数说明
# -s：输出调试信息，包括print打印的信息。
# -v：显示更详细的信息。
# -q：显示简略的结果 与-v相反
# -p no:warnings 过滤警告
# -n=num：启用多线程或分布式运行测试用例。需要安装 pytest-xdist 插件模块。
# -k=value：用例的nodeid包含value值则用例被执行。
# -m=标签名：执行被 @pytest.mark.标签名 标记的用例。
# -x：只要有一个用例执行失败就停止当前线程的测试执行。
# --maxfail=num：与-x功能一样，只是用例失败次数可自定义。
# --reruns=num：失败用例重跑num次。需要安装 pytest-rerunfailures 插件模块。
# -l: 展示运行过程中的全局变量和局部变量
# --collect-only: 罗列出所有当前目录下所有的测试模块，测试类及测试函数
# --ff: 如果上次测试用例出现失败的用例，当使用--ff后，失败的测试用例会首先执行，剩余的用例也会再次执行一次 *基于生成了.pytest_cache文件
# --lf: 当一个或多个用例失败后，定位到最后一个失败的用例重新运行，后续用例会停止运行。*基于生成了.pytest_cache文件
# --html=report.html: 在当前目录生成名为report.html的测试报告 需要安装 pytest-html 插件模块。
