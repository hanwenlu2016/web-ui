# -*- coding: utf-8 -*-
# @File: setting.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/28  9:20


########## 通用配置
CASE_TYPE = 'web'  # 项目类型  'app'  # web

IS_CLEAN_REPORT = False  # 是否清除 测试历史测试报告结果 * 默认清除

IS_REDIS = False  # 是否读取redis 数据 (完成代码用列后导入管理平台时使用) 默认不读取 #False/True

########## selenium/appium配置
IMPLICITLY_WAIT_TIME = 10  # 显示等待最长时间 /s

POLL_FREQUENCY = 0.2  # 显示等待元素出现时 在此时间内检索一次 /s

########## 接口端配置
API_URL = "https://github.com/"  # "https://github.com/" #'"http://192.168.7.101/api"  # 接口地址

TIMEOUT = 5  # 接口请求超时时间 /S

HEADERS = {'Content-Type': 'application/json',}

########## Web端配置
URL = "http://192.168.7.95/caac/#/login"  # # 项目地址 web 时选择

BROWSERNAME = "Chrome"  # "Chrome" "Firefox" "Ie"  "Safari"  # 浏览器选择

IS_COLONY = False  # 是否启动集群模式 True(启用)  False(不启用)

HUB_HOST = '192.168.7.101:4444'  # 集群hub地址和端口

########## 移动端配置
PLATFORM = 'Android'  # 'Android'  # ios Android  平台 app 时配合

APIUMHOST = '192.168.203.17:4723'  # appium 服务器地址

ANDROID_CAPA = {"platformName": PLATFORM,
                "platformVersion": "6.0.1",  # 系统版本
                "deviceName": '127.0.0.1:5555',  # 设备名称  网易MUMU模拟器	默认5555
                "appPackage": "com.tencent.mm",  # app包名
                "appActivity": "com.tencent.mm.ui.LauncherUI",  # 启动页面 *
                "autoLaunch": True,  # 测试时是否需要自动运行app  * 必须要开启
                "autoGrantPermissions": True,  # 让appium自动授权app权限，如果noReset为True，则该条不生效。
                "newCommandTimeout": 60,  # 为了结束Appium会话，会设置一个等待从客户端发送命令的超时时间，默认为60秒，一般不需要设置
                "deviceReadyTimeout": 60,  # 等待设备就绪的时间
                "unicodeKeyboard": True, # 使用 unicodeKeyboard 的编码方式来发送字符串
                "noReset": True,  # 启动app时不要清除app里的原有的数据
                }  # 安卓参数

IOS_CAPA = {
    "platformName": PLATFORM,  # *
    "platformVersion": '14.1',  # 系统版本 *
    "deviceName": 'Redad',  # 设备名称 *
    "automationName": "XCUITest",
    "bundleId": "com.redaflight.RedaSkyPoint22a",  # app包名 *
    "udid": "5235c499f02839759fccc412fdb4c50920ef5244",  # 手机UDID *
    "xcodeOrgId": "J4397KG4TG",  # 开发者id *
    "xcodeSigningId": "iPhone Developer",
    "useNewWDA": False,
    "noReset": True,  # 启动app时不要清除app里的原有的数据
    "newCommandTimeo": 60
}  # IOS参数

########## DB 配置
MYSQL = {'user': 'root', 'password': 'root', 'port': 3306, 'host': '127.0.0.1', 'db': 'demotest'}

ORACLE = {'user': 'cdm', 'password': 'cdm', 'host': '192.168.7.1:1521/ORCL'}

REDIS = {'host': '127.0.0.1', 'port': '6379', 'password': '', 'db': 1}

# redis 集群配置
REDIS_CLUSTER = [{'host': '192.168.7.1', 'port': 7000}, {'host': '192.168.7.1', 'port': 7002},
                 {'host': '192.168.7.2', 'port': 7000}, {'host': '192.168.7.2', 'port': 7001},
                 {'host': '192.168.7.3', 'port': 7001}, {'host': '192.168.7.3', 'port': 7001}]

REDIS_CLUSTER_PASWORD = ''
