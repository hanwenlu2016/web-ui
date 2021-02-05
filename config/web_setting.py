# -*- coding: utf-8 -*-
# @File: web_setting.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/14  11:17

import os
import sys

# 框架基础路径  不需要修改
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 项目地址
URL = "https://192.168.7.51/portal/#"

# 浏览器配置
BROWSERNAME = "Chrome"  # "Chrome" "Firefox" "Ie"  "Safari"


######### 浏览器驱动 参数配置 ########

# 谷歌浏览器驱动路径
WIN_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "windos", "chromedriver.exe")
LUINX_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "linux", "chromedriver")
MAC_CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "mac", "chromedriver")


# 系统判断
OS_JUDGMENT = sys.platform.lower()

# 如果windos 使用 WIN_CHROMEDRIVER 如果是  linux 使用 LUINX_CHROMEDRIVER 其它就用 MAC_CHROMEDRIVER
CHROMEDRIVER_PATH = lambda: WIN_CHROMEDRIVER if OS_JUDGMENT == 'win32' else (
    LUINX_CHROMEDRIVER if OS_JUDGMENT == 'linux' else MAC_CHROMEDRIVER)

CHROMEDRIVER = CHROMEDRIVER_PATH()  # 实际谷歌浏览器路径



# 火狐浏览器驱动路径
WIN_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "windos", "geckodriver.exe")
LUINX_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "linux", "geckodriver")
MAC_FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "mac", "geckodriver")

FIREFOXDRIVER_PATH = lambda: WIN_FIREFOXDRIVER if OS_JUDGMENT == 'win32' else (
    LUINX_FIREFOXDRIVER if OS_JUDGMENT == 'linux' else MAC_FIREFOXDRIVER)

FIREFOXDRIVER = FIREFOXDRIVER_PATH()  # 实际火狐浏览器驱动

# IE浏览驱动路径
IEDRIVER = os.path.join(BASE_DIR, "driver", "windos", "IEDriverServer.exe")

#  Safari  浏览独有 默认自带驱动无须配置
