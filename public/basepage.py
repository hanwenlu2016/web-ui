# -*- coding: utf-8 -*-
# @File: selenium_driver.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/11/4  14:40

import os
import time
import pyautogui, pyperclip
import allure
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from public.logs import logger
from config.setting import PRPORE_SCREEN_DIR, IMPLICITLY_WAIT_TIME, POLL_FREQUENCY



class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        """
        获取当前页面  title
        :return:
        """
        title = self.driver.title
        logger.info(f"获取当前title {title}")
        return title

    def get_url(self):
        """
        获取当前页面的URL
        :return:
        """
        currentURL = self.driver.current_url
        logger.info(f"获取当前url {currentURL}")
        return currentURL

    def get_url_html(self):
        """
        获取当前页面 html内容
        :return:
        """
        sourceHtml = self.driver.page_source
        logger.info(f"获取当前html {sourceHtml}")
        return sourceHtml

    def refresh(self):
        """
        刷新当前页面
        :return:
        """
        logger.info('刷新当前页面')
        return self.driver.refresh()

    def back(self):
        """
        返回上一个页面
        :return:
        """
        self.driver.back()
        logger.info('返回上一个页面')

    def forward(self):
        """
        前进到下一个页面
        :return:
        """
        self.driver.forward()
        logger.info('前进到下一个页面')

    def web_scroll(self, direction):
        """
        网页滚动
        :param direction: str   up 向上   Down 向下
        :return:
        """
        if direction == "up":
            logger.info('滚动到顶部')
            self.driver.execute_script("window.scrollBy(0, -10000);")
        if direction == "down":
            logger.info('滚动到底部')
            self.driver.execute_script("window.scrollBy(0, 10000)")

    def current_window(self):
        """
        获取当前窗口句柄 不能单一使用 实际获取的不是当前句柄
        :return:
        """
        current_window = self.driver.current_window_handle
        logger.info(f'获取当前句柄 {current_window}')
        return current_window

    def all_handle(self):
        """
        获取所有句柄
        :return:  list
        """
        handle = self.driver.window_handles
        logger.info(f'获取所有句柄 {handle}')
        return handle

    def switch_windows(self, index):
        """
        多窗口切换
        :param index: 列表索引 all_handle的列表索引位置
        :return:
        """
        indexHandle = self.all_handle()[index]
        try:
            logger.info(f'窗口已经切换{indexHandle}')
            return self.driver.switch_to_window(indexHandle)

        except Exception as e:
            logger.error("查找窗口句柄handle异常-> {0}".format(e))

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
        获取定位类型
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
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        elif locatorType == "partlink":
            return By.PARTIAL_LINK_TEXT
        elif locatorType == "tag":
            return By.TAG_NAME
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

    def clicks(self, locatorType, locator):
        """
        获取元素后  左键点击
        :param locatorType: 定位类型
        :param locator: 定位器
        :return:
        """
        element = self.get_element(locatorType, locator)
        element.click()

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

    def send_keys(self, data, locatorType, locator):
        """
        获取元素后输入
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
        self.send_keys(data, locatorType, locator)

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
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
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

    def save_as_img(self, locatorType, locator, filename, sleep=1):
        """
        图片另存为  下载文件也可以直接使用
        :param locatorType: 定位类型
        :param locator: 定位器
        :param filename: 图片名称 路径必须要输入正确 以为函数没办法判断是否成功
        :param sleep: 等待windo 窗口时间 默认 1 秒
        :return: str path 文件路径
        """
        # 右键点击
        self.rightClick(locatorType, locator)
        # 图片另存为
        pyautogui.typewrite(['V'])

        # 将地址以及文件名复制
        pic_dir = os.path.join(PRPORE_SCREEN_DIR, f'{filename}.jpg')
        pyperclip.copy(pic_dir)

        # 等待窗口打开，以免命令冲突，粘贴失败，试过很多次才有0.8，具体时间自己试
        time.sleep(sleep)

        # 粘贴
        pyautogui.hotkey('ctrlleft', 'V')

        # 保存
        pyautogui.press('enter')
        logger.info(f'图片路径为{filename}！')
        return pic_dir

    def upload_files(self, locatorType, locator, filepath, sleep=1):
        """
        文件上传
        :param locatorType: 定位类型
        :param locator: 定位器
        :param filepath: 文件路径 路径必须要输入正确 以为函数没办法判断是否成功
        :param sleep: 等待windo 窗口时间 默认 1 秒
        :return:
        """
        element = self.get_element(locatorType, locator)
        element.click()
        time.sleep(sleep)

        # pyautogui.write(filepath)  # 不支持中文路径

        # 支持中文路径
        pyperclip.copy(filepath)
        time.sleep(sleep)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('enter', presses=2)
        logger.info(f'上传文件路径{filepath}')


# x = BasePage(WebBrowserDriver.opt())
# x.upload_files('id', 'calbtn', r'D:\My-Svn-oprject\reda-ui-auto\output\report_screen\我.png')
