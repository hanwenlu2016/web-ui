# -*- coding: utf-8 -*-
# @File: setting.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/28  9:20

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 是否清除 测试历史测试报告结果 * 默认清除
IS_CLEAN_REPORT = True

# 是否读取redis 数据 (完成代码用列后导入管理平台时使用) 默认不读取
IS_REDIS = False


# 项目地址

URL = "https://www.baidu.com/"
# URL = "https://tool.jisuapi.com/pic2base64.html"

# 浏览器配置
BROWSERNAME = "Chrome"  # "Firefox" "Ie"

## selenium 配置

# 隐形等待最长时间 /s
IMPLICITLY_WAIT_TIME = 10

# 隐形等待元素出现时 在此时间内检索一次 /s
POLL_FREQUENCY = 0.5

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, "log")

# 测试用例结果目录
PRPORE_JSON_DIR = os.path.join(BASE_DIR, "output", "report_json")

# 测试结果报告目录
PRPORE_ALLURE_DIR = os.path.join(BASE_DIR, "output", "report_allure")

# 测试截图目录
PRPORE_SCREEN_DIR = os.path.join(BASE_DIR, "output", "report_screen")

# 测试用例集目录
CASE_DIR = os.path.join(BASE_DIR, "case")

# 测试数据 yaml用例目录
DATA_YAML = os.path.join(BASE_DIR, "database", "yaml")

# 测试数据 文件目录
DATA_FILE = os.path.join(BASE_DIR, "database", "file")

# 浏览器驱动路径
CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "chromedriver.exe")
FIREfoxDRIVER = os.path.join(BASE_DIR, "driver", "geckodriver.exe")
IEDRIVER = os.path.join(BASE_DIR, "driver", "IEDriverServer.exe")

# 数据库信息配置

MYSQL = {'user': 'root', 'password': 'root', 'port': 3306, 'host': '127.0.0.1', 'db': 'fdr'}

ORACLE = {'user': 'cdm', 'password': 'cdm', 'host': '192.168.7.158:1521/ORCL'}

REDIS = {'host': '192.168.203.5', 'port': '6379', 'password': '', 'db': 1}

# redis 集群配置
REDIS_CLUSTER = [{'host': '192.168.7.51', 'port': 7000}, {'host': '192.168.7.52', 'port': 7000},
                 {'host': '192.168.7.53', 'port': 7000}, {'host': '192.168.7.51', 'port': 7001},
                 {'host': '192.168.7.52', 'port': 7001}, {'host': '192.168.7.53', 'port': 7001}]


REDIS_CLUSTER_PASWORD = ''

# 打码平台API信息  页面需要登录验证码时 启用
# 账号 密码 打码软件id api地址
IMG_INFO = {'username': '', 'password': '', 'code_id': 909536,
            'api_url': 'http://upload.chaojiying.net/Upload/Processing.php'}
