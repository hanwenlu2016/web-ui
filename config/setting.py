# -*- coding: utf-8 -*-
# @File: setting.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/28  9:20


import  os ,sys


# 运行用列类型 (app、web)
CASE_TYPE ='app' #'app'  # web

# -----selenium/appium  配置
# 显示等待最长时间 /s
IMPLICITLY_WAIT_TIME = 10

# 显示等待元素出现时 在此时间内检索一次 /s
POLL_FREQUENCY = 0.2


# 是否清除 测试历史测试报告结果 * 默认清除
IS_CLEAN_REPORT = True

# 是否读取redis 数据 (完成代码用列后导入管理平台时使用) 默认不读取
IS_REDIS = False

# 框架基础路径  不需要修改
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志路径
LOG_DIR = os.path.join(BASE_DIR, "log")

### 测试用例集路径
# APP/WEB用列目录
APP_CASE_DIR = os.path.join(BASE_DIR, "case", "appcase")
WEB_APP_CASE_DIR = os.path.join(BASE_DIR, "case", "webcase")

# 如果用列类型等于app 就返回app的用列目录 否则返回web的
CASEPATH = lambda: APP_CASE_DIR if CASE_TYPE.lower() == 'app' else WEB_APP_CASE_DIR
CASE_DIR = CASEPATH()

### yaml测试用列数据路径
# APP/WEB YAML数据
APP_YAML_DIR = os.path.join(BASE_DIR, "database", "yaml","app", )
WEB_YAML_DIR = os.path.join(BASE_DIR, "database","yaml" ,"web" )

# 如果用列类型等于app 就返回app的YAML 否则返回web的
DATA_YAML = lambda: APP_YAML_DIR if CASE_TYPE.lower() == 'app' else WEB_YAML_DIR
YAML_DIR = DATA_YAML()




### 测试文件路径
# APP/WEB flie数据
DATA_FILE_APP = os.path.join(BASE_DIR, "database", "file", "app")
DATA_FILE_WEB = os.path.join(BASE_DIR, "database", "file", "web")

# 如果用列类型等于app 就返回app的测试文件 否则返回web的
DATA_FILE = lambda: DATA_FILE_APP if CASE_TYPE.lower() == 'app' else DATA_FILE_WEB
DATA_DIR = DATA_FILE()

# 测试用例结果目录
PRPORE_JSON_DIR = os.path.join(BASE_DIR, "output", "report_json")

# 测试结果报告目录
PRPORE_ALLURE_DIR = os.path.join(BASE_DIR, "output", "report_allure")

# 测试截图目录
PRPORE_SCREEN_DIR = os.path.join(BASE_DIR, "output", "report_screen")

# 数据库信息配置
MYSQL = {'user': 'root', 'password': 'root', 'port': 3306, 'host': '127.0.0.1', 'db': 'fdr'}

ORACLE = {'user': 'cdm', 'password': 'cdm', 'host': '192.168.7.158:1521/ORCL'}

REDIS = {'host': '192.168.203.5', 'port': '6379', 'password': '', 'db': 1}

# redis 集群配置
REDIS_CLUSTER = [{'host': '192.168.7.51', 'port': 7000}, {'host': '192.168.7.52', 'port': 7000},
                 {'host': '192.168.7.53', 'port': 7000}, {'host': '192.168.7.51', 'port': 7001},
                 {'host': '192.168.7.52', 'port': 7001}, {'host': '192.168.7.53', 'port': 7001}]

REDIS_CLUSTER_PASWORD = 'reda2019'

# 打码平台API信息  页面需要登录验证码时 启用
# 账号 密码 打码软件id api地址
IMG_INFO = {'username': '', 'password': '', 'code_id': 909536,
            'api_url': 'http://upload.chaojiying.net/Upload/Processing.php'}
