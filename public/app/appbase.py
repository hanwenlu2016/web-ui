# -*- coding: utf-8 -*-
# @File: appbase.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/14  15:52


import os
import time

import allure
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction

from public.logs import logger
from config.setting import PRPORE_SCREEN_DIR
from config.web_setting import POLL_FREQUENCY, IMPLICITLY_WAIT_TIME


class Base():

    def __init__(self, driver):
        self.driver = driver

    def accept(self):
        """
        警告框处理 确认
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.accept()
            logger.info('警告框已确认')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def dismiss(self):
        """
        警告框处理  取消
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.dismiss()
            logger.info('警告框已取消')
            return accept
        except Exception as e:
            logger.error("查找dismiss弹出框异常-> {0}".format(e))

    def alertText(self):
        """
        警告框处理 提取警告框文本
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.text
            logger.info(f'警告框文本信息为 {accept}')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def screen_shot(self, doc):
        """
        截取当前界面图片
        :param doc:  str 名称
        :return:
        """
        fileName = doc + "." + str(round(time.time() * 1000)) + ".png"
        if len(fileName) >= 200:
            fileName = str(round(time.time() * 1000)) + ".png"
        filePath = os.path.join(PRPORE_SCREEN_DIR, fileName)

        self.driver.save_screenshot(filePath)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=fileName,
                      attachment_type=allure.attachment_type.PNG)
        logger.info(f"截图成功已经存储在: {filePath}")

    def get_by_type(self, locatorType):
        """
        获取定位类型  目前 app 只提供了 ，id，name，xpath，class
        :param locatorType:  str  in(id,name,xpath,css,class,link,partlink,tag)
        :return:  False
        """
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "class":
            return By.CLASS_NAME
        else:
            logger.info(f"Locator type {locatorType} not correct/supported")
        return False

    def get_element(self, locatorType, locator):
        """
        获取元素  此函数配合 isElementExist 检查元素是否存在
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        byType = self.get_by_type(locatorType)
        if self.isElementExist(byType, locator):
            element = self.driver.find_element(byType, locator)
            return element
        else:
            logger.error('定位元素错误未找到！')
            return None

    def clicks(self, locatorType, locator):
        """
        获取元素后  左键点击
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        element = self.get_element(locatorType, locator)
        element.click()

    def base_click(self):
        """
        点击页面
        :return:
        """
        base_click = self.driver.click()

        return base_click

    def rightClick(self, locatorType, locator):
        """
        获取元素后 右键点击
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        element = self.get_element(locatorType, locator)

        ActionChains(self.driver).context_click(element).perform()

    def doubleClick(self, locatorType, locator):
        """
        获取元素后 双击击
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        element = self.get_element(locatorType, locator)

        ActionChains(self.driver).double_click(element).perform()

    def input_keys(self, data, locatorType, locator):
        """
        获取元素后输入 并支持键盘操作  from selenium.webdriver.common.keys import Keys  Keys.ENTER ..
        :param data: str 测试数据
        :param locatorType: 定位类型
        :param locator: 定位器
        :param element:
        :return:
        """
        element = self.get_element(locatorType, locator)
        element.send_keys(data)

    def clear(self, locatorType, locator):
        """
        清除输入框
        :param locatorType:  定位类型
        :param locator: 定位器
        :return:
        """
        element = self.get_element(locatorType, locator)
        element.clear()

    def clear_send_keys(self, data, locatorType, locator):
        """
        输入前   清除输入框
        :param data:  输入测试数据
        :param locatorType: 定位类
        :param locator: 定位器
        :return:
        """
        self.clear(locatorType, locator)
        self.input_keys(data, locatorType, locator)

    def get_dropdown_options_count(self, locatorType, locator):
        """
        获取下拉选项的个数
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """

        element = self.get_element(locatorType, locator)
        sel = Select(element)
        options = sel.options
        return options

    def get_text(self, locatorType, locator):
        """
        获取文本内容
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        text = self.get_element(locatorType, locator).text
        logger.info(f"获取文本 {text}")
        return text

    def element_hover(self, locatorType, locator):
        """
        获取元素后悬停到元素位置
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        element = self.get_element(locatorType, locator)
        hover = ActionChains(self.driver).move_to_element(element).perform()
        logger.info(f"鼠标悬停位置{locator}")

    def element_hover_clicks(self, locatorType, locator):
        """
        获取元素后悬停到元素位置 后点击该元素
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        element = self.get_element(locatorType, locator)
        hover = ActionChains(self.driver).move_to_element(element).perform()
        self.clicks(locatorType, locator)
        logger.info(f"鼠标悬停位置{locator}")

    def isElementDisplayed(self, locatorType, locator):
        """
        检查元素是否可见
        :param locatorType:定位类型
        :param locator: 定位器
        :param element:
        :return:
        """
        isDisplayed = False
        element = None

        if locator:
            element = self.get_element(locatorType, locator)
        if element is not None:
            isDisplayed = element.is_displayed()
            logger.info(f"Element is displayed with locator: {locator} and locatorType: {locatorType}")
        else:
            logger.error(f"Element is not displayed with locator: {locator} and locatorType: {locatorType}")
        return isDisplayed

    def isElementExist(self, locatorType, locator):
        """
        检查元素是否存在
        :param locatorType: 定位类型 get_element 函数传递过来
        :param locator: 定位器
        :return:
        """
        if self.waitForElement(locatorType, locator) != False:
            elementList = self.driver.find_elements(locatorType, locator)
            if len(elementList) > 0:
                logger.info("找到元素")
                return True
            else:
                logger.info("元素未找到")
                return False

    def waitForElement(self, locatorType, locator):
        """
        等待元素被加载  配合 isElementExist 函数检查元素是否存在
        :param locatorType: 定位类型  get_element 函数传递过来
        :param locator:  定位器
        :return:
        """
        timeout = IMPLICITLY_WAIT_TIME
        poll = POLL_FREQUENCY
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll)

            element = wait.until(EC.presence_of_element_located((locatorType, locator)))
            logger.info(f'等待页面元素 {locator} {locatorType}  存在')
            return element
        except Exception as e:
            logger.error('等待元素错误,元素在隐形等待时间内未出现！')
            logger.error(e)
            return False

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

    def tap_click(self, x, y):
        """
        坐标点击
        :param x: x点
        :param y: y点
        :return:
        """
        act = TouchAction(self.driver)
        act.tap(x=x, y=y).perform()

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
