# -*- coding: utf-8 -*-
# @File: appsetting.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/14  10:05

# 设备系统
PLATFORMNAME = 'Android'  # ios

# 设备系统版本
PLATFORMVERSION = '7'

# 设备名称  adb devices 名称查看
DEVICENAME = '127.0.0.1:62001 device'

# 测试app包名
APPPACKAGE = 'com.jingdong.app.mall'

#
APPACTIVITY = 'main.MainActivity'

# 测试时是否需要自动运行app  * 必须要开启
AUTOLAUNCH = True

# 让appium自动授权app权限，如果noReset为True，则该条不生效。
AUTOGRANTPERMISSIONS = True

# 为了结束Appium会话，会设置一个等待从客户端发送命令的超时时间，默认为60秒，一般不需要设置
NEWCOMMANDTIMEOUT = 60

# 等待设备就绪的时间
DEVICEREADYTIMEOUT = 60

# 启动app时不要清除app里的原有的数据
NORESET = True

# appium 服务器地址
APIUMHOST = '192.168.203.5'

# apium 端口
APIUMPORT = '4723'

# 组合连接信息字典
CAPABILITIES = {"platformName": PLATFORMNAME,
                "platformVersion": PLATFORMVERSION,
                "deviceName": DEVICENAME,
                "appPackage": APPPACKAGE,
                "appActivity": APPACTIVITY,
                "autoLaunch": AUTOLAUNCH,
                "autoGrantPermissions": AUTOGRANTPERMISSIONS,
                "newCommandTimeout": NEWCOMMANDTIMEOUT,
                "deviceReadyTimeout": DEVICEREADYTIMEOUT,
                "noReset": NORESET,
                }
