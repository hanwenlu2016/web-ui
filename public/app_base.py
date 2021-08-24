# -*- coding: utf-8 -*-
# @File: appbase.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/3/18  18:16

"""
-- locate定位说明   ** app 定位方式
    -- 通用：  AccessibilityId 、class(安卓对应 ClassName / iso对应 type) 、 xpath  * 公共的只支持 3种
    -- 安卓：  uiautomator(*定位最快 不支持 iso) 、AccessibilityId(安卓对应 content-desc / iso对应 abel和name属性)  、
              class(ClassName) 、 id(resource-id)  、xpath  * 安卓只支持5种
    -- ios： ios_predicate(*定位最快 不支持安卓) 、AccessibilityId(安卓对应 content-desc / iso对应 abel和name属性) 、
             class(安卓对应 ClassName / iso对应 type) 、xpath * ios只支持4种
--operate 操作说明：
    input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) , slide(滑动)   * 只支持 6种

-- appexe 函数
定位类型支持 : uiautomator 、ios_predicate 、accessibilityid、xpath、class、id
操作方式支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、slide(滑动)
"""

import os
import time
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction

from public.reda_data import  GetCaseYmal
from public.common import ErrorExcep,logger
from config.ptahconf import PRPORE_SCREEN_DIR
from config.setting import POLL_FREQUENCY, IMPLICITLY_WAIT_TIME, PLATFORM


class Base:

    def __init__(self, driver, ):
        self.driver = driver

    @property
    def dri(self):
        return self.driver

    def sleep(self, s: float):
        """
        休眠秒数
        :param s:
        :return:
        """
        time.sleep(s)
        logger.info('强制休眠{}'.format(s))

    def device_x_get(self):
        """
        获取分辨率 宽
        :return:
        """
        return self.driver.get_window_size()['width']

    def device_y_get(self):
        """
       获取分辨率 高
       :return:
       """
        return self.driver.get_window_size()['height']

    def get_size(self):
        """
        获取屏幕分辨率
        :return:
        """

        rect = self.driver.get_window_size()
        return rect['width'], rect['height']

    def add_volume(self, frequency=1):
        """
        增加声音 ** 可以搜索 keyevent 查询具体参数
        :param frequency: 增加次数 默认一次
        :return:
        """
        logger.warning('此函数只支持安卓系统！')
        for i in range(0, frequency):
            self.dri.keyevent(24)

    def reduce_volume(self, frequency=1):
        """
        减小声音
        :param frequency: 减小次数 默认一次
        :return:
        """
        logger.warning('此函数只支持安卓系统！')
        for i in range(0, frequency):
            self.dri.keyevent(25)

    def back(self, ):
        """
        返回键
        :param
        :return:
        """
        return self.dri.keyevent(4)

    def uesd_keyevent(self, code):
        """
        发送 keyevent 操作  * 可以百度搜索 keyevent键列表
        :param code:  keyevent码
        :return:
        """
        logger.warning('此函数只支持安卓系统！')
        self.dri.keyevent(code)

    def locks(self, s):
        """
        锁定屏幕
        :param s: 锁定的秒数
        :return:
        """
        self.dri.lock(s)

    def background_apps(self, s):
        """
        把 app 放到后台
        :param s: 放置几秒
        :return:
        """
        logger.warning('此函数只支持安卓系统！')
        self.dri.background_app(s)

    def open_notification(self, ):
        """
        打开菜单栏
        :return:
        """
        logger.warning('此函数只支持安卓系统！')
        return self.dri.open_notifications()

    def install_app(self, apppath):
        """
        安装app
        :param path: app 路径
        :return:
        """
        self.dri.install_app(apppath)

    def delete_app(self, app):
        """
        删除app
        :param app: app 包名
        :return:
        """
        self.dri.remove_app(app)

    def is_app_install(self, app):
        """
        检查app 是否安装
        :param app: app 包名
        :return: True/False
        """
        return self.dri.is_app_installed(app)

    def tap_click(self, element=None, x=None, y=None):
        """
        点击  如果 element x y 都传递 使用element  and vice versa
        :param element：  定位的元素
        :param x: x点
        :param y: y点
        :return:
        """
        act = TouchAction(self.driver)

        act.tap(element=element, x=x, y=y).perform()

    def press_s(self, element=None, x=None, y=None, ):
        """
        按下 指定秒数
        :param element: 定位的元素   如果 element x y 都传递 使用element  and vice versa
        :param x:
        :param y:
        :param s: 默认按下1秒
        :return:
        """
        pre = TouchAction(self.driver)
        pre.long_press(el=element, x=x, y=y).perform()
        # pre.press(el=element, x=x, y=y).perform()

    def right_to_left_move_to(self, press_el=None, press_x=0, press_y=0, mo_el=None, mo_x=0, mo_y=0):
        """
        指定位置 从x点到y点
        :param press_el:
        :param press_x:
        :param press_y:
        :param mo_el:
        :param mo_x:
        :param mo_y:
        :return:
        """

        right_to_left = TouchAction(self.driver)

        (right_to_left
         .press(press_el, x=press_x, y=press_y)
         .wait(1000).move_to(mo_el, x=mo_x, y=mo_y)
         .release().perform())

    def swipe_left(self, swipe_times=1):
        """
        向左滑动
        :param swipe_times:
        :return:
        """
        logger.info("向左滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]

        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.8, height * 0.5, width * 0.2, height * 0.5, duration=800)
            time.sleep(0.5)

    def swipe_right(self, swipe_times=1):
        """
        向右滑动
        :param swipe_times:
        :return:
        """
        logger.info("向右滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.2, height * 0.5, width * 0.8, height * 0.5)
            time.sleep(0.5)

    def swipe_up(self, swipe_times=1):
        """
        向上滑动
        :param swipe_times:
        :return:
        """
        logger.info("向上滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.5, height * 0.2, width * 0.5, height * 0.8)
            time.sleep(0.5)

    def swipe_down(self, swipe_times=1):
        """
        向下滑动
        :param swipe_times:
        :return:
        """
        logger.info("向下滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.5, height * 0.8, width * 0.5, height * 0.2)
            time.sleep(0.5)

    def scroll_page_one_time(self, direction="up", swipe_times=1):
        """
        屏幕滑动 几次
        :param direction: 方向
            up: 从下往上
            down: 从上往下
            left: 从右往左
            right: 从左往右
        :param swipe_times: 默认1次
        """

        screen_size = self.driver.get_window_size()
        screen_width = screen_size["width"]
        screen_height = screen_size["height"]

        center_x = screen_width * 0.5
        center_y = screen_height * 0.5

        top_x = center_x
        top_y = screen_height * 0.25
        down_x = center_x
        down_y = screen_height * 0.75
        left_x = screen_width * 0.25
        left_y = center_y
        right_x = screen_width * 0.75
        right_y = center_y

        if direction == "up":
            for i in range(0, swipe_times):
                self.driver.swipe(down_x, down_y, top_x, top_y, 2000)
                time.sleep(0.5)
        elif direction == "down":
            for i in range(0, swipe_times):
                self.driver.swipe(top_x, top_y, down_x, down_y, 2000)
                time.sleep(0.5)
        elif direction == "left":
            for i in range(0, swipe_times):
                self.driver.swipe(right_x, right_y, left_x, left_y, 2000)
                time.sleep(0.5)
        elif direction == "right":
            for i in range(0, swipe_times):
                self.driver.swipe(left_x, left_y, right_x, right_y, 2000)
                time.sleep(0.5)
        else:
            logger.error("请输入正确的参数 up、left、right、down")
            raise Exception("请输入正确的参数 up、left、right、down")

    def screen_shot(self, doc, imgreport=True):
        """
        截取当前界面图片
        :param doc:  str 名称
        :param imgreport:  str 图片追加到测试报告 默认添加到报告
        :return:
        """
        fileName = doc + "_" + str(round(time.time() * 1000)) + ".png"
        if len(fileName) >= 200:
            fileName = str(round(time.time() * 1000)) + ".png"
        filePath = os.path.join(PRPORE_SCREEN_DIR, fileName)

        self.driver.save_screenshot(filePath)
        if imgreport:
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=fileName,
                          attachment_type=allure.attachment_type.PNG)
        logger.info(f"截图成功已经存储在: {filePath}")
        return filePath


class CommonlyUsed(Base):
    """
     常用定位方式  class(安卓对应 ClassName / iso对应 type) 、 xpath 、 id、
    """

    def get_by_type(self, types):
        """
        获取定位类型  目前 app 只提供了 ，
        *安卓 (id(resource-id), class(ClassName) , xpath,)
        *iso (xpath, class(type) ,cont_name(name) , )
        :param types:  str
        :return:  False
        """
        types = types.lower()
        if types == "id":
            if PLATFORM.lower() == 'android':
                logger.warning('此方法只支持android系统,ios不支持建议更换定位方式！！')
                return By.ID
            else:
                logger.error(f'{PLATFORM} 不支持id定位')
        elif types == "xpath":
            return By.XPATH
        elif types == "class":
            return By.CLASS_NAME
        else:
            logger.info(f"Locator type {types} not correct/supported")

        raise ErrorExcep(f'不支持输入类型参数{types}！！！')

    def used_operate(self, types, locate, el=None):
        """
        获取元素  此函数配合 isElementExist 检查元素是否存在
        :param types: 定位类型
        :param locator: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :return: driver 对象
        """
        types = self.get_by_type(types)
        if self.isElementExist(types, locate):
            if el is not None:
                # find_element 不为空时 查询多个
                element = self.driver.find_elements(types, locate)
            else:
                # find_element 为空时 查询单个
                element = self.driver.find_element(types, locate)
            return element
        else:
            logger.error('定位元素错误未找到！')

    def used_text(self, types, locate, index=None):
        """
        获取元素  提取文本内容
        :param types: 定位类型
        :param locator: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :return: driver 对象
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        types = self.get_by_type(types)

        if self.isElementExist(types, locate):

            if el is not None and index is not None:
                # 多个定位
                return self.used_operate(types=types, locate=locate, el=el)[index].text
            else:
                # 单个定位提取文本元素必须是唯一 如果多个时默认返回第一个
                return self.used_operate(types=types, locate=locate).text
        else:
            logger.error('定位元素错误未找到！')

    def used_click(self, types, locate, index=None):
        """
        获取元素后  点击
        :param types: 定位类型
        :param locator: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        if el is not None and index is not None:
            # 多个定位定位 利用index 列表索引点击
            self.used_operate(types=types, locate=locate, el=el)[index].click()
        else:
            # 单个定位点击
            self.used_operate(types=types, locate=locate).click()

    def used_input(self, types, locate, text, index=None):
        """
        获取元素后输入 并支持键盘操作
        :param types: 定位类型
        :param locate:  定位元素或者 表达式
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'
        if el is not None and index is not None:
            self.used_operate(types=types, locate=locate, el=el)[index].send_keys(text)
        else:
            self.used_operate(types=types, locate=locate, ).send_keys(text)

    def used_clear(self, types, locate, index=None):
        """
        清除输入框
        :param types: 定位类型
        :param locator: 定位元素
        :param index: 列表索引位置  find_element传递时 此值必填
        """

        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'
        if el is not None and index is not None:
            self.used_operate(types=types, locate=locate, el=el)[index].clear()
        else:
            self.used_operate(types=types, locate=locate).clear()
        logger.warning('此定位方法只android系统！！！')

    def used_clear_continue_input(self, types, locate, text, index=None):
        """
        清除数据在输入
        :param types: 定位类型
        :param locator: 定位元素
        :param text: 输入文本
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """

        self.used_clear(types=types, locate=locate, index=index)
        time.sleep(0.5)
        self.used_input(types=types, locate=locate, text=text, index=index)

    def isElementDisplayed(self, types, locate):
        """
        检查元素是否可见
        :param types:定位类型
        :param locate: 定位器
        :param element:
        :return:
        """
        isDisplayed = False
        element = None

        if locate:
            element = self.used_operate(types, locate)
        if element is not None:
            isDisplayed = element.is_displayed()
            logger.info(f"Element is displayed with locate: {locate} and types: {types}")
        else:
            logger.error(f"Element is not displayed with locate: {locate} and types: {types}")
        return isDisplayed

    def isElementExist(self, types, locate):
        """
        检查元素是否存在
        :param types: 定位类型 used_operate 函数传递过来
        :param locate: 定位器
        :return:
        """
        if self.waitForElement(types, locate):
            elementList = self.driver.find_elements(types, locate)
            if len(elementList) > 0:
                logger.info(f"找到元素 {locate}")
                return True
            else:
                logger.info("元素未找到")
                return False

    def waitForElement(self, types, locate):
        """
        等待元素被加载  配合 isElementExist 函数检查元素是否存在
        :param types: 定位类型  used_operate 函数传递过来
        :param locate:  定位器
        :return:
        """
        timeout = IMPLICITLY_WAIT_TIME
        poll = POLL_FREQUENCY

        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll)
            element = wait.until(EC.presence_of_element_located((types, locate)))
            logger.info(f'等待页面元素 {locate} {types}  存在')
            return element
        except Exception:
            logger.error('等待元素错误,元素在等待时间内未出现！')
            raise ErrorExcep('等待元素错误,元素在等待时间内未出现！')


class AndroidUiautomatorBase(Base):
    """
     安卓  find_elements_by_android_uiautomator 操作封装类
    """

    def android_uiautomator(self, locate, el=None):
        """
         更具表达式 查询页面元素
        此方法 只能安卓可用
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :return: str drive对象
        """
        try:
            logger.warning('此定位方法只android系统！！！')
            if el is not None:
                # 多个定位
                # android_uiautomator_driver = self.driver.find_elements_by_android_uiautomator(locate)
                return WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                     poll_frequency=POLL_FREQUENCY).until(
                    lambda x: x.find_elements_by_android_uiautomator(locate))

            else:
                # 单个定位
                # return self.driver.find_element_by_android_uiautomator(locate)
                return WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                     poll_frequency=POLL_FREQUENCY).until(
                    lambda x: x.find_element_by_android_uiautomator(locate))

        except Exception as e:
            logger.error(f'元素在显示等待时间 {IMPLICITLY_WAIT_TIME} 未出现！请检查元素是否存在！！')

    def android_uiautomator_text(self, locate, index=None):
        """
         更具表达式 查询页面元素 并获取文本内容
        此方法 只能安卓可用
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
        :param index: 列表索引位置  find_element传递时 此值必填
        :return: str  text 文本内容
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'

        if el is not None and index is not None:
            # 多个定位
            return self.android_uiautomator(locate=locate, el=el)[index].text
        else:
            # 单个定位提取文本元素必须是唯一 如果多个时默认返回第一个
            return self.android_uiautomator(locate=locate, el=el).text

    def android_uiautomator_click(self, locate, index=None):
        """
        更具表达式 查询页面元素 并点击
        此方法 只能安卓可用
       :param locate:  locate 表达式 如 :new UiSelector().text("显示")
       :param index: 列表索引位置  find_element传递时 此值必填
       :return: str drive对象
       """
        el = None
        if index is not None:
            el = 'l'

        if el is not None and index is not None:
            # 多个定位定位 利用index 列表索引点击
            self.android_uiautomator(locate=locate, el=el)[index].click()
        else:
            # 单个定位点击
            self.android_uiautomator(locate).click()

    def android_uiautomator_input(self, locate, text, index=None):
        """
        更具表达式 查询页面元素 并输入 文本
        此方法 只能安卓可用
       :param locate:  locate 表达式 如 :new UiSelector().text("显示")
       :param index: 列表索引位置  find_element传递时 此值必填
       :return: str drive对象
       """
        el = None
        if index is not None:
            el = 's'  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个

        if el is not None and index is not None:
            self.android_uiautomator(locate, el=el)[index].send_keys(text)
        else:
            self.android_uiautomator(locate).send_keys(text)
        logger.warning('此定位方法只android系统！！！')

    def android_uiautomator_clear(self, locate, index=None):
        """
        更具表达式 查询页面元素 并 清除操作
        此方法 只能安卓可用
       :param locate:  expression 表达式 如 :new UiSelector().text("显示")
       :param index: 列表索引位置  find_element传递时 此值必填
       :return: str drive对象
       """
        el = None
        if index is not None:
            el = 's'  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个

        if el is not None and index is not None:
            self.android_uiautomator(locate, el=el)[index].clear()
        else:
            self.android_uiautomator(locate).clear()
        logger.warning('此定位方法只android系统！！！')

    def android_uiautomator_clear_continue_input(self, locate, text, index=None):
        """
        更具表达式 查询页面元素 并 清除内容 在进行输入
        此方法 只能安卓可用
       :param locate:  expression 表达式 如 :new UiSelector().text("显示")
       :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
       :param index: 列表索引位置  find_element传递时 此值必填
       :return:
       """

        self.android_uiautomator_clear(locate=locate, index=index)
        time.sleep(0.5)
        self.android_uiautomator_input(locate=locate, text=text, index=index)


class IosPredicate(Base):
    """
    iso 封装 find_elements_by_ios_predicate 操作封装类
    """

    def ios_predicate(self, locate, el=None):
        """
         更具表达式 查询页面元素
        此方法 只能 iso 可用
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :return: str drive对象
        """
        try:
            logger.warning('此定位方法只ios系统！！！')
            if el is not None:
                # ios_predicate = self.driver.find_elements_by_ios_predicate(locate)
                ios_predicate = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                              poll_frequency=POLL_FREQUENCY).until(
                    lambda x: x.find_elements_by_ios_predicate(locate))  # 在显示登陆时间内查询元素
            else:
                # ios_predicate = self.driver.find_element_by_ios_predicate(locate)
                ios_predicate = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                              poll_frequency=POLL_FREQUENCY).until(
                    lambda x: x.find_element_by_ios_predicate(locate))
            return ios_predicate
        except Exception as e:
            logger.error(f'元素在显示等待时间 {IMPLICITLY_WAIT_TIME} 未出现！请检查元素是否存在！！ {e}')

    def ios_predicate_text(self, locate, index=None):
        """
         更具表达式 查询页面元素
        此方法 只能 iso 可用
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return: str drive对象
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        logger.warning('此定位方法只ios系统！！！')
        if el is not None and index is not None:
            return self.driver.find_elements_by_ios_predicate(locate=locate, el=el)[index].text
        else:
            return self.driver.find_element_by_ios_predicate(locate=locate, el=el).text

    def ios_predicate_click(self, locate, index=None):
        """
         更具表达式 查询页面元素 并且点击该元素
        此方法 只能 iso 可用
        :param locate:  locate 表达式 如 :new UiSelector().text("显示")
       :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
       :param index: 列表索引位置  find_element传递时 此值必填
       :return: str drive对象
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        logger.warning('此定位方法只ios系统！！！')
        if el is not None and index is not None:
            # 多个定位定位 利用index 列表索引点击
            self.ios_predicate(locate=locate, el=el)[index].click()
        else:
            # 单个定位点击
            self.ios_predicate(locate=locate).click()

    def ios_predicate_input(self, locate, text, index=None):
        """
         更具表达式 查询页面元素 并且输入文本
        此方法 只能 iso 可用
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
       :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
       :param index: 列表索引位置  find_element传递时 此值必填
       :return: str drive对象
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'
        logger.warning('此定位方法只ios系统！！！')
        if el is not None and index is not None:
            self.ios_predicate(locate=locate, el=el)[index].send_keys(text)
        else:
            self.ios_predicate(locate=locate).send_keys(text)

    def ios_predicate_clear(self, locate, index=None):
        """
         更具表达式 查询页面元素 并且清除输入文本
        此方法 只能 iso 可用
         :param locate:  expression 表达式 如 :new UiSelector().text("显示")
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return: str drive对象
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'
        logger.warning('此定位方法只ios系统！！！')
        if el is not None and index is not None:
            self.ios_predicate(locate=locate, el=el)[index].clear()
        else:
            self.ios_predicate(locate=locate, el=el).clear()

    def ios_predicate_clear_continue_input(self, locate, text, index=None):
        """
         更具表达式 查询页面元素  先清除 后输入
        此方法 只能 iso 可用
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
       :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
       :param index: 列表索引位置  find_element传递时 此值必填
       :return:
        """

        self.ios_predicate_clear(locate=locate, index=index)
        time.sleep(0.5)
        self.ios_predicate_input(locate=locate, text=text, index=index)


class AccessibilityId(Base):
    """
    AccessibilityId 类封装
    """

    def accessibility_id(self, locate, el=None):
        """
        AccessibilityId 元素定位
        Android ：  Android的content-desc属性对应AccessibilityId
        Ios :  IOS的label和name属性都对应AccessibilityId定位方式
        :param locate: 定位元素
        :param find_element: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :return: 返回定位到的元素 driver
        """
        try:
            if el is not None:
                # accessibilityId = self.driver.find_elements_by_accessibility_id(locate)
                accessibilityId = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                                poll_frequency=POLL_FREQUENCY).until(
                    lambda x: x.find_elements_by_accessibility_id(locate))  # 在显示等待时间去查询元素
            else:
                # accessibilityId = self.driver.find_element_by_accessibility_id(locate)
                accessibilityId = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                                poll_frequency=POLL_FREQUENCY).until(
                    lambda x: x.find_element_by_accessibility_id(locate))

            return accessibilityId
        except Exception as e:
            logger.error(f'元素在显示等待时间 {IMPLICITLY_WAIT_TIME} 未出现！请检查元素是否存在！！ {e}')

    def accessibility_id_text(self, locate, index=None):
        """
        AccessibilityId 元素定位
        Android ：  Android的content-desc属性对应AccessibilityId
        Ios :  IOS的label和name属性都对应AccessibilityId定位方式
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return: str  text 文本内容r
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        if el is not None and index is not None:
            return self.driver.find_elements_by_accessibility_id(locate=locate, el=el)[index].text
        else:
            return self.driver.find_element_by_accessibility_id(locate=locate, el=el).text

    def accessibility_id_click(self, locate, index=None):
        """
        AccessibilityId 元素定位  并点击该元素
        Android ：  Android的content-desc属性对应AccessibilityId
        Ios :  IOS的label和name属性都对应AccessibilityId定位方式
        :param locate:  locate 表达式 如 :new UiSelector().text("显示")
       :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
       :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """

        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        if el is not None and index is not None:
            self.accessibility_id(locate=locate, el=el)[index].click()
        else:
            self.accessibility_id(locate).click()

    def accessibility_id_input(self, locate, text, index=None):
        """
        AccessibilityId 元素定位  并点击该元素
        Android ：  Android的content-desc属性对应AccessibilityId
        Ios :  IOS的label和name属性都对应AccessibilityId定位方式
        :param locate: 定位元素
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        if el is not None and index is not None:
            self.accessibility_id(locate=locate, el=el)[index].send_keys(text)
        else:
            self.accessibility_id(locate).send_keys(text)

    def accessibility_id_clear(self, locate, index=None):
        """
        AccessibilityId 元素定位  并清除文本内容
        Android ：  Android的content-desc属性对应AccessibilityId
        Ios :  IOS的label和name属性都对应AccessibilityId定位方式
        :param locate:  expression 表达式 如 :new UiSelector().text("显示")
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
       :param index: 列表索引位置  find_element传递时 此值必填
       :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        if el is not None and index is not None:
            self.accessibility_id(locate, el=el)[index].clear()
        else:
            self.accessibility_id(locate).clear()

    def accessibility_id_clear_continue_input(self, locate, text, index=None):
        """
        AccessibilityId 元素定位  并清除文本内容 继续输入
        Android ：  Android的content-desc属性对应AccessibilityId
        Ios :  IOS的label和name属性都对应AccessibilityId定位方式
         :param locate:  expression 表达式 如 :new UiSelector().text("显示")
       :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
       :param index: 列表索引位置  find_element传递时 此值必填
       :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 's'

        self.accessibility_id_clear(locate=locate, index=index)
        time.sleep(0.5)
        self.accessibility_id_input(locate=locate, text=text, index=index)


class AppBase(AccessibilityId, AndroidUiautomatorBase, IosPredicate, CommonlyUsed):

    def __if_android_operate_uiautomator(self, locate, operate=None, text=None, index=None):
        """
        * 私有不继承
        判断 uiautomator 执行操作
        :param locate:  表达 或者定位元素
        :param operate: 执行操作、 类型input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) , slide(滑动)
        :param text: 输入文本内容
        :param index:
         android_uiautomator_click 、android_uiautomator_text、android_uiautomator_input、android_uiautomator_clear、
         列表索引位置  find_element传递时 此值必填
         scroll_page_one_time index 传递滑动次数

        :return:
        """
        if operate is None:
            el = index  # 如果index 为空默认多个
            return self.android_uiautomator(locate=locate, el=el)

        if operate in ('text', 'click', 'input', 'clear', 'clear_continue_input', 'slide'):
            if operate == 'text':  # 提取文本

                return self.android_uiautomator_text(locate=locate, index=index)

            elif operate == 'click':  # 点击操作

                self.android_uiautomator_click(locate=locate, index=index)

            elif operate == 'input':  # 输入操作
                if text is not None:
                    return self.android_uiautomator_input(locate=locate, text=text, index=index)
                logger.error('android_uiautomator_input 函数必须传递 text 参数')

            elif operate == 'clear':  # 清除操作

                return self.android_uiautomator_clear(locate=locate, index=index)

            elif operate == 'clear_continue_input':  # 清除后在输入操作
                if text is not None:
                    return self.android_uiautomator_clear_continue_input(locate=locate, text=text, index=index)
                logger.info('android_uiautomator_clear_continue_input 函数必须传递 text 参数')

            elif operate == 'slide':  # 滑动操作
                if index is None:
                    index = 1
                self.scroll_page_one_time(direction=locate, swipe_times=index)

        else:
            logger.error(f""" uiautomator不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、
                slide(滑动) """)
            raise ErrorExcep(
                f""" uiautomator不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、
                slide(滑动) """)

    def __if_operate_ios_predicate(self, locate, operate=None, text=None, index=None):
        """
        * 私有不继承
        判断 ios_predicate操作执行
        :param locate:  expression 表达式 如 :ios_predicate  name=="个人统计"
        :param operate: 执行操作、 类型input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) , slide(滑动)
        :param text: 输入文本内容

        :param index:
         android_uiautomator_click 、android_uiautomator_text、android_uiautomator_input、android_uiautomator_clear、
         列表索引位置  find_element传递时 此值必填
         scroll_page_one_time index 传递滑动次数
        :return:
        """
        if operate is None:
            el = index  # 如果index 为空默认多个
            return self.ios_predicate(locate=locate, el=el)
        if operate in ('text', 'click', 'input', 'clear', 'clear_continue_input', 'slide'):
            if operate == 'text':  # 提取文本

                return self.ios_predicate_text(locate=locate, index=index)

            elif operate == 'click':  # 点击操作

                return self.ios_predicate_click(locate=locate, index=index)

            elif operate == 'input':  # 输入操作
                if text is not None:
                    self.ios_predicate_input(locate=locate, text=text, index=index)
                logger.error('ios_predicate_input 函数必须传递 text 参数')

            elif operate == 'clear':  # 清除操作

                self.ios_predicate_clear(locate=locate, index=index)

            elif operate == 'clear_continue_input':  # 清除后在输入操作

                self.ios_predicate_clear_continue_input(locate=locate, text=text, index=index)

            elif operate == 'slide':  # 滑动操作
                if index is None:
                    index = 1
                self.scroll_page_one_time(direction=locate, swipe_times=index)
        else:
            logger.error(f""" ios_predicate不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、
                slide(滑动) """)
            raise ErrorExcep(
                f""" ios_predicate不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、
                    slide(滑动) """)

    def __if_acceaaibilityid_predicate(self, locate, operate=None, text=None, index=None):
        """
        * 私有不继承
        判断 accessibilityid执行操作
        :param locate:  表达 或者定位元素
        :param operate: 执行操作 类型input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) , slide(滑动)
        :param text: 输入文本内容
        :return:
        """
        if operate is None:
            el = index  # 如果index 为空默认多个
            return self.accessibility_id(locate=locate, el=el)
        if operate in ('text', 'click', 'input', 'clear', 'clear_continue_input', 'slide'):
            if operate == 'text':  # 提取文本、多个时需要传递index 参数

                self.accessibility_id_text(locate=locate, index=index)

            elif operate == 'click':  # 点击操作 、多个时需要传递index 参数

                self.accessibility_id_click(locate=locate, index=index)

            elif operate == 'input':  # 输入操作 、 多个时需要传递index 参数
                if text is not None:
                    self.accessibility_id_input(locate=locate, text=text, index=index)
                logger.error('accessibility_id_input 函数必须传递 text 参数')

            elif operate == 'clear':  # 清除操作

                self.accessibility_id_clear(locate=locate, index=index)

            elif operate == 'clear_continue_input':  # 清除后在输入操作
                if text is not None:
                    self.accessibility_id_clear_continue_input(locate=locate, text=text, index=index)

            elif operate == 'slide':  # 滑动操作
                if index is None:
                    index = 1
                self.scroll_page_one_time(direction=locate, swipe_times=index)

        else:
            logger.error(f""" accessibilityid不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、
                slide(滑动) """)
        raise ErrorExcep(
            f""" accessibilityid不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、
                slide(滑动) """)

    def __if_commonly_used_predicate(self, types, locate, operate=None, text=None, index=None, ):
        """
        * 私有不继承
        判断 CommonlyUsed 执行操作
        :param locate:  表达 或者定位元素
        :param operate: 执行操作 类型input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) , slide(滑动)
        :param text: 输入文本内容
        :return:
        """
        if operate is None:
            el = index  # 如果index 为空默认多个
            return self.used_operate(types=types, locate=locate, el=el)
        if operate in ('text', 'click', 'input', 'clear', 'clear_continue_input', 'slide'):
            if operate == 'text':  # 提取文本

                return self.used_text(types=types, locate=locate, index=index)

            elif operate == 'click':  # 点击操作

                self.used_click(types=types, locate=locate, index=index)

            elif operate == 'input':  # 输入操作
                if text is not None:
                    return self.used_input(types=types, locate=locate, text=text, index=index)
                logger.error('android_uiautomator_input 函数必须传递 text 参数')

            elif operate == 'clear':  # 清除操作

                return self.used_clear(types=types, locate=locate, index=index)

            elif operate == 'clear_continue_input':  # 清除后在输入操作
                if text is not None:
                    return self.used_clear_continue_input(types=types, locate=locate, text=text, index=index)
                logger.info('android_uiautomator_clear_continue_input 函数必须传递 text 参数')

            elif operate == 'slide':  # 滑动操作
                if index is None:
                    index = 1
                self.scroll_page_one_time(direction=locate, swipe_times=index)
        else:
            logger.error(f""" CommonlyUsed不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、
               """)
            raise ErrorExcep(
                f""" CommonlyUsed不支持输入参数{operate}！！ 目前只支持：input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)、slide(滑动)
               """)

    def app_expression(self, types, locate, operate=None, text=None, index=None, wait=0.2, notes=None):
        """

        app  执行操作判断
        安卓 ios 表达式定位方法  (uiautomator(安卓) / ios_predicate(ios)  accessibilityid(安卓/ios))
        :param types: 定位类型
        :param locate: 表达 或者定位元素
        安卓  'new UiSelector().text("显示")'
        iOS  "type == 'XCUIElementTypeButton' AND value == 'ClearEmail'"
        :param operate: 执行操作  input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) , slide(滑动)   * 只支持 6种
        :param text : 输入文本内容
        :param index:
        :param wait: 默认 等待0.5 秒
        :param notes: 注释操作说明
        :return:
        """
        if types in ('uiautomator', 'ios_predicate', 'accessibilityid', 'xpath', 'class', 'id'):
            # 只支持安卓
            if PLATFORM.lower() == 'android' and types == 'uiautomator':
                logger.warning('此方法只支持android系统！！')
                logger.info(notes)
                return self.__if_android_operate_uiautomator(locate=locate, operate=operate, text=text,
                                                             index=index,
                                                             )

            # 只支持 iso
            elif PLATFORM.lower() == 'ios' and types == 'ios_predicate':
                logger.warning('此方法只支持ios系统！！')
                logger.info(notes)
                return self.__if_operate_ios_predicate(locate=locate, operate=operate, text=text, index=index,
                                                       )

            elif types == 'accessibilityid':
                logger.info(notes)
                return self.__if_acceaaibilityid_predicate(locate=locate, operate=operate, text=text, index=index
                                                           )

            elif types in ('xpath', 'class', 'id'):
                logger.info(notes)
                return self.__if_commonly_used_predicate(types=types, locate=locate, operate=operate, text=text,
                                                         index=index)
        else:

            logger.error(f"""输入的{types}操作类型，暂时不支持！！
            uiautomator 、ios_predicate 、accessibilityid、xpath、class、id 定位类型
            """)
            raise ErrorExcep(f"""输入的{types}操作类型，暂时不支持！！
            uiautomator 、ios_predicate 、accessibilityid、xpath、class、id 定位类型
            """)

    def appexe(self, yamlfile, case, text=None, index=None, wait=0.1):
        """
        自动执行定位步骤
        :param yamlfile:  yaml文件
        :param case: yaml定位用例
        :param text:  输入内容
        :param el:  是否为多个  el='l' 多个
        :param index:
        :param wait:  等待多少
        :return:
        """
        relust = None  # 断言结果  最后一步才返回

        locator_data = self.get_locator(yamlfile, case)
        locator_step = locator_data.stepCount()

        for locator in range(0, locator_step):
            if isinstance(text, list) and (
                    locator_data.operate(locator) == 'input' or locator_data.operate(
                locator) == 'clear_continue_input'):
                relust = self.app_expression(types=locator_data.types(locator), locate=locator_data.locate(locator),
                                             operate=locator_data.operate(locator), notes=locator_data.info(locator),
                                             text=text[locator],
                                             index=index)
            else:
                relust = self.app_expression(types=locator_data.types(locator), locate=locator_data.locate(locator),
                                             operate=locator_data.operate(locator), notes=locator_data.info(locator),
                                             text=text,
                                             index=index)
            time.sleep(wait)

        return relust

    def get_loca(self, yaml_names=None, case_names=None,):
        """
        获取定位步骤用例数据
        :param yaml_names: ymal 路径
        :param case_names:  用例名称
        :param case_names: 默认读取 locatorYAML 路径数据 FLASE 读取CASEYMAL_DIR
        :return:
        """
        if yaml_names is not None:
            return GetCaseYmal(yaml_name=yaml_names, case_name=case_names)
        else:
            raise ErrorExcep('yaml路径不能为空！')
