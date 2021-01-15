# -*- coding: utf-8 -*-
# @File: web_setting.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/14  11:17

import os

# 框架基础路径  不需要修改
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 项目地址
URL = "https://192.168.7.51/portal/#"

# 浏览器配置
BROWSERNAME = "Chrome"  # "Firefox" "Ie"

# -----selenium 配置

# 显示等待最长时间 /s
IMPLICITLY_WAIT_TIME = 10

# 显示等待元素出现时 在此时间内检索一次 /s
POLL_FREQUENCY = 0.5

# 浏览器驱动路径
CHROMEDRIVER = os.path.join(BASE_DIR, "driver", "chromedriver.exe")  # 谷歌

FIREFOXDRIVER = os.path.join(BASE_DIR, "driver", "geckodriver.exe")  # 火狐

IEDRIVER = os.path.join(BASE_DIR, "driver", "IEDriverServer.exe")  # IE
