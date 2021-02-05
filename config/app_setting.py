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
# 测试app包名
APP ='com.jingdong.app.mall' # 安卓appPackage / ios bundleId


# appium 服务器地址
APIUMHOST = '192.168.203.5'

# apium 端口
APIUMPORT = '4723'

# 组合连接信息字典
CAPABILITIES = {"platformName": PLATFORMNAME,
                "platformVersion": PLATFORMVERSION,
                "deviceName": DEVICENAME,
                "appPackage": APP,  # app包名
                "appActivity": 'main.MainActivity', # 启动页面 *
                "autoLaunch": True,
                "autoGrantPermissions": True,
                "newCommandTimeout": 60, # 为了结束Appium会话，会设置一个等待从客户端发送命令的超时时间，默认为60秒，一般不需要设置
                "deviceReadyTimeout": 60, # 等待设备就绪的时间
                "noReset": True, # 启动app时不要清除app里的原有的数据
                }

# IOS参数
IOS_CAPA = {
    "platformName": PLATFORMNAME, # *
    "platformVersion": PLATFORMVERSION, # *
    "deviceName": DEVICENAME, # *
    "automationName": "XCUITest",
    "bundleId": APP, # *
    "udid": "", # 手机UDID *
    "xcodeOrgId": "", # 开发者id *
    "xcodeSigningId": "iPhone Developer",
    "useNewWDA": False,
    "noReset": True, # 启动app时不要清除app里的原有的数据
    "newCommandTimeo": 60
}

# 判断系统返回对应的参数
isCAPA = lambda: IOS_CAPA if PLATFORMNAME.lower() == "ios" else ANDROID_CAPA

CAPA = isCAPA()
