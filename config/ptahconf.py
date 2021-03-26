# -*- coding: utf-8 -*-
# @File: ptahconf.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/2/8  13:45

import  os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


######### 浏览器驱动 参数配置 ######## 可用绝对路劲  LUINX_CHROMEDRIVER='/use/bin/chromedriver'  线上建议
# LUINX 系统浏览器驱动路劲
LUINX_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "linux", "chromedriver")  # 谷歌浏览器
LUINX_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "linux", "geckodriver") # 火狐浏览器

# windos 系统浏览器驱动路劲
IE_PATH = os.path.join(BASE_DIR, "driver", "windos", "IEDriverServer.exe") # ie浏览器
WIN_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "windos", "chromedriver.exe") # 谷歌浏览器
WIN_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "windos", "geckodriver.exe") # 火狐浏览器

# mac 系统浏览器驱动路劲
MAC_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "mac", "chromedriver") # 谷歌浏览器
MAC_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "mac", "geckodriver") # 火狐浏览器


# 日志路径----------------------------
LOG_DIR = os.path.join(BASE_DIR, "log")

### 测试用例集路径

CASE_DIR = os.path.join(BASE_DIR, "case", )

### yaml测试用列数据路径
YAML_DIR = os.path.join(BASE_DIR, "database", "yaml", )

### 测试文件路径
DATA_FILE = os.path.join(BASE_DIR, "database", "file")

# 测试用例结果目录
PRPORE_JSON_DIR = os.path.join(BASE_DIR, "output", "report_json")

# 测试结果报告目录
PRPORE_ALLURE_DIR = os.path.join(BASE_DIR, "output", "report_allure")

# 测试截图目录
PRPORE_SCREEN_DIR = os.path.join(BASE_DIR, "output", "report_screen")


