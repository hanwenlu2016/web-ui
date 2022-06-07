# -*- coding: utf-8 -*-
# @File: __init__.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/2/5  14:29
import os

__all__ = ['BASE_DIR', 'LUINX_CHROMEDRIVER', 'LUINX_FIREFOXDRIVER', 'IE_PATH', 'WIN_CHROMEDRIVER',
           'WIN_FIREFOXDRIVER', 'MAC_CHROMEDRIVER', 'MAC_FIREFOXDRIVER', 'LOG_DIR', 'CASE_DIR',
           'CASEYMAL_DIR', 'LOCATORYMAL_DIR', 'DATA_FILE', 'DIFF_IMGPATH', 'STETING_YAML_DIR',
           'PRPORE_JSON_DIR', 'PRPORE_ALLURE_DIR', 'PRPORE_SCREEN_DIR', 'PRPORE_TMP'
           ]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

######### 浏览器驱动 参数配置 ######## 可用绝对路劲  LUINX_CHROMEDRIVER='/use/bin/chromedriver'  线上建议
# LUINX 系统浏览器驱动路劲
LUINX_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "linux", "chromedriver")  # 谷歌浏览器
LUINX_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "linux", "geckodriver")  # 火狐浏览器

# windos 系统浏览器驱动路劲
IE_PATH = os.path.join(BASE_DIR, "driver", "windos", "IEDriverServer.exe")  # ie浏览器
WIN_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "windos", "chromedriver.exe")  # 谷歌浏览器
WIN_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "windos", "geckodriver.exe")  # 火狐浏览器

# mac 系统浏览器驱动路劲
MAC_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "mac", "chromedriver")  # 谷歌浏览器
MAC_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "mac", "geckodriver")  # 火狐浏览器

# 日志路径----------------------------
LOG_DIR = os.path.join(BASE_DIR, "log")

### 测试用例集路径

CASE_DIR = os.path.join(BASE_DIR, "case", )

### yaml测试用列数据路径
CASEYMAL_DIR = os.path.join(BASE_DIR, "database", "caseYAML", )  # 测试数据
LOCATORYMAL_DIR = os.path.join(BASE_DIR, "database", "locatorYAML", )  # 定位数据

### 测试文件路径
DATA_FILE = os.path.join(BASE_DIR, "database", "file")

# 测试图片断言路径
DIFF_IMGPATH = os.path.join(BASE_DIR, "database", "file", "img")

# 测试用例结果目录
PRPORE_JSON_DIR = os.path.join(BASE_DIR, "output", "report_json")

# 测试结果报告目录
PRPORE_ALLURE_DIR = os.path.join(BASE_DIR, "output", "report_allure")

# 测试截图目录
PRPORE_SCREEN_DIR = os.path.join(BASE_DIR, "output", "report_screen")

# 测试截图目录
STETING_YAML_DIR = os.path.join(BASE_DIR, "config", "setting.yaml")

# 测试临时目录
PRPORE_TMP = os.path.join(BASE_DIR, "output", "report_tmp")
