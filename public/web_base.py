# -*- coding: utf-8 -*-
# @File: selenium_driver.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/11/4  14:40

import os
import sys
import time
from enum import Enum
from typing import TypeVar, Optional

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from config import PRPORE_SCREEN_DIR
from public.common import ErrorExcep, logger, is_assertion, reda_conf
from public.reda_data import GetCaseYmal, replace_py_yaml

EM = TypeVar('EM')  # 可以是任何类型。

# 读取配置参数
WEB_UI = reda_conf('WEB_UI')
WEB_POLL_FREQUENCY = WEB_UI.get('WEB_WIMPLICITLY_WAIT_TIME')
WEB_IMPLICITLY_WAIT_TIME = WEB_UI.get('WEB_POLL_FREQUENCY')

# 读取配置参数
APP_UI = reda_conf('APP_UI')
APP_POLL_FREQUENCY = APP_UI.get('APP_POLL_FREQUENCY')
APP_IMPLICITLY_WAIT_TIME = APP_UI.get('APP_IMPLICITLY_WAIT_TIME')
PLATFORM = APP_UI.get('APP_PLATFORM')

# 读取 项目类型
CASE_TYPE = reda_conf('CURRENCY').get('CASE_TYPE')

if CASE_TYPE.lower() == 'web':
    POLL_FREQUENCY = WEB_POLL_FREQUENCY
    IMPLICITLY_WAIT_TIME = WEB_IMPLICITLY_WAIT_TIME
else:
    POLL_FREQUENCY = APP_POLL_FREQUENCY
    IMPLICITLY_WAIT_TIME = APP_IMPLICITLY_WAIT_TIME


class Locaate(Enum):
    """
    定位类型枚举类
        定位类型
                types 对应selenium 的操作
                web 8中  function为函数类型
          types                              selenium
          (/ 代表或者 link_text or link > LINK_TEXT)
          "id"                            >   ID
          "xpath"                         >   XPATH
          "link_text/link"                >   LINK_TEXT
          "partial_link_text/partial"     >   PARTIAL_LINK_TEXT
          "name"                          >   NAME
          "tag_name/tag"                  >   TAG_NAME
          "class_name/class"              >   CLASS_NAME
          "css_selector/css"              >   CSS_SELECTOR
          "function"                      >   web_html_content 或 web_url web_title
                app    web(8)+ app 7中  15
        "accessibility_id"        >    ACCESSIBILITY_ID       --对应检测器 android 对应 content-desc和accessibilityid/iso对应labe和name属性accessibilityid
        "android_uiautomator"     >      ANDROID_UIAUTOMATOR  --对应检测器 java 语法 new UiSelector().text("显示")
        "android_viewtag"         >      ANDROID_VIEWTAG
        "android_datamatcher"     >      ANDROID_DATA_MATCHER
        "android_viewmatcher"     >      ANDROID_VIEW_MATCHER
        "ios_predicate"           >      IOS_PREDICATE   -- 对应检测器ios predicate
        "ios_class_chain"         >      IOS_CLASS_CHAIN -- 对应检测器ios class chain

        建议使用推荐  ** xpath消耗性能 app定位时尽量不使用 xpath
        *安卓 (android_uiautomator、android_viewtag、android_datamatcher、android_viewmatcher、resource-id、 id 、xpath )
        *iso (ios_predicate 、ios_class_chain 、resource-id、xpath)

    """
    web_types = ['id', 'xpath', 'link_text', 'link', 'partial_link_text', 'partial', 'name', 'tag_name',
                 'tag', 'class_name', 'class', 'css_selector', 'css', 'function']

    app_types = ['id', 'xpath', 'link_text', 'link', 'partial_link_text', 'partial', 'name', 'tag_name',
                 'tag', 'class_name', 'class', 'css_selector', 'css', 'function', 'accessibility_id', 'ios_predicate',
                 'ios_class_chain', 'android_uiautomator', 'android_viewtag',
                 'android_datamatcher', 'android_viewmatcher']


class Operation(Enum):
    """
       操作类型:
       操作类型                                    执行动作
       input                       >               输入
       click                       >               点击
       text                        >               提取文本
       submit                      >               提交
       scroll                      >               滑动下拉
       clear                       >               清除
       jsclear                     >               js清除
       jsclear_continue_input      >               js清除后输入
       clear_continue_input        >               清除在输入
       web_url                     >               获取当前url
       web_title                   >               获取当前title
       web_html_content            >               获取html内容
       iframe                      >               跳转到iframe

       slide                       >              滑动屏幕 (只支持app)
       """

    web_operation = ['input', 'click', 'text', 'submit', 'scroll', 'clear',
                     'jsclear', 'jsclear_continue_input', 'clear_continue_input',
                     'web_url', 'web_title', 'web_html_content', 'iframe']

    app_operation = ['input', 'click', 'text', 'submit', 'scroll', 'clear',
                     'jsclear', 'jsclear_continue_input', 'clear_continue_input',
                     'web_url', 'web_title', 'web_html_content', 'iframe', 'slide']


class Base:

    def __init__(self, driver):
        self.driver = driver

    def web_by(self, types: str) -> EM or None:
        """
        获取定位类型
        :param types:  str  in(id,xpath,link_text/link,partial_link_text/partial,name,
        tag_name/tag,class_name/class,css_selector/css)
        :return:
        """
        types = types.lower()
        locate_typess = Locaate.web_types.value

        if types not in locate_typess:
            logger.error(f'web目前只支持{locate_typess}')
            raise ErrorExcep('操作类型不支持')

        if types == "id":
            return By.ID
        elif types == "xpath":
            return By.XPATH
        elif types == "link_text" or types == "link":
            return By.LINK_TEXT
        elif types == "partial_link_text" or types == "partial":
            return By.PARTIAL_LINK_TEXT
        elif types == "name":
            return By.NAME
        elif types == "tag_name" or types == "tag":
            return By.TAG_NAME
        elif types == "class_name" or types == "class":
            return By.CLASS_NAME
        elif types == "css" or types == "css_selector":
            return By.CSS_SELECTOR
        elif types == "function":
            return types

        else:
            logger.error(f"web目前只支持{types}")
            raise Exception('定位类型错误！！！！')

    def app_by(self, types: str) -> EM or None:
        """
                定位类型
                types 对应selenium 的操作
                web 8中  function为函数类型
          types                              selenium
          (/ 代表或者 link_text or link > LINK_TEXT)
          "id"                            >   ID
          "xpath"                         >   XPATH
          "link_text/link"                >   LINK_TEXT
          "partial_link_text/partial"     >   PARTIAL_LINK_TEXT
          "name"                          >   NAME
          "tag_name/tag"                  >   TAG_NAME
          "class_name/class"              >   CLASS_NAME
          "css_selector/css"              >   CSS_SELECTOR
          "function"                      >   web_html_content 或 web_url web_title
                    app 7中
        "accessibility_id"        >    ACCESSIBILITY_ID       --对应检测器 android 对应 content-desc和accessibilityid/iso对应labe和name属性accessibilityid
        "android_uiautomator"     >      ANDROID_UIAUTOMATOR  --对应检测器 java 语法 new UiSelector().text("显示")
        "android_viewtag"         >      ANDROID_VIEWTAG
        "android_datamatcher"     >      ANDROID_DATA_MATCHER
        "android_viewmatcher"     >      ANDROID_VIEW_MATCHER
        "ios_predicate"           >      IOS_PREDICATE   -- 对应检测器ios predicate
        "ios_class_chain"         >      IOS_CLASS_CHAIN -- 对应检测器ios class chain

        建议使用推荐  ** xpath消耗性能 app定位时尽量不使用 xpath
        *安卓 (android_uiautomator、android_viewtag、android_datamatcher、android_viewmatcher、resource-id、 id 、xpath )
        *iso (ios_predicate 、ios_class_chain 、resource-id、xpath)
        :param types:  str
        :return:
        """

        types = types.lower()
        app_locate_typess = Locaate.app_types.value

        if types not in app_locate_typess:
            logger.error(f'app目前只支持{app_locate_typess}')
            raise ErrorExcep('操作类型不支持')

        if types == "accessibility_id":
            return AppiumBy.ACCESSIBILITY_ID

        elif types == "ios_predicate" and PLATFORM.lower() == 'ios':
            return AppiumBy.IOS_PREDICATE

        elif types == "ios_class_chain" and PLATFORM.lower() == 'ios':
            return AppiumBy.IOS_CLASS_CHAIN

        elif types == "android_uiautomator" and PLATFORM.lower() == 'android':
            return AppiumBy.ANDROID_UIAUTOMATOR

        elif types == "android_viewtag" and PLATFORM.lower() == 'android':
            return AppiumBy.ANDROID_VIEWTAG

        elif types == "android_datamatcher" and PLATFORM.lower() == 'android':
            return AppiumBy.ANDROID_DATA_MATCHER

        elif types == "android_viewmatcher" and PLATFORM.lower() == 'android':
            return AppiumBy.ANDROID_VIEW_MATCHER

        elif types == "id":
            return By.ID
        elif types == "xpath":
            return By.XPATH
        elif types == "link_text" or types == "link":
            return By.LINK_TEXT
        elif types == "partial_link_text" or types == "partial":
            return By.PARTIAL_LINK_TEXT
        elif types == "name":
            return By.NAME
        elif types == "tag_name" or types == "tag":
            return By.TAG_NAME
        elif types == "class_name" or types == "class":
            return By.CLASS_NAME
        elif types == "css" or types == "css_selector":
            return By.CSS_SELECTOR
        elif types == "function":
            return types
        else:
            logger.error(f'app目前只支持{app_locate_typess}')
            raise Exception('定位类型错误！！！！')

    def get_by_type(self, types: str) -> EM or None:
        """
        判断 APP or WEB   by类型
        :param types:   定位类型
        :return:
        """
        if CASE_TYPE.lower() == 'web':
            return self.web_by(types)
        else:
            return self.app_by(types)

    @property
    def web_title(self):
        """
        获取当前web_页面  title
        :return:
        """
        title = self.driver.title
        logger.debug(f"获取当前title {title}")
        return title

    @property
    def web_url(self):
        """
        获取当前web_页面的URL
        :return:
        """
        url = self.driver.current_url
        logger.debug(f"获取当前url {url}")
        return url

    @property
    def web_html_content(self):
        """
        获取当前web页面 html内容
        :return:
        """
        content = self.driver.page_source
        logger.debug('获取当前HTML内容')
        return content

    def sleep(self, s: float) -> float or int:
        """
        休眠秒数
        :param s:
        :return:
        """
        if s:
            logger.debug('强制等待 {} /s'.format(s))
            time.sleep(s)
        else:
            pass

    def web_refresh(self):
        """
        刷新当前页面
        :return:
        """
        logger.debug('刷新当前页面')
        return self.driver.refresh()

    def web_back(self):
        """
        返回上一个页面
        :return:
        """
        logger.debug('返回上一个页面')
        return self.driver.back()

    def web_forward(self):
        """
        前进到下一个页面
        :return:
        """
        logger.debug('前进到下一个页面')
        return self.driver.forward()

    def web_baclick(self):
        """
        点击页面
        :return:
        """

        base_click = self.driver.click()
        logger.debug('点击当前页面')
        return base_click

    def web_scroll(self, direction: str) -> None:
        """
        网页滚动 部分网页不可用时轻请使用  web_scroll_to_ele
        :param direction: str   up 向上   Down 向下
        :return:
        """
        if direction == "up":
            logger.debug('滚动到顶部')
            self.driver.execute_script("window.scrollBy(0, -10000);")
        if direction == "down":
            logger.debug('滚动到底部')
            self.driver.execute_script("window.scrollBy(0, 10000)")

    def web_scroll_to_ele(self, types: str, locate: str, index: int = None) -> None:
        """
        滚动至元素ele可见位置
        :param types: 定位类型
        :param locate: 定位器
        :param index: 多个标签索引
        :return:
        """
        el = None
        if index is not None:
            el = 's'
        target = self.driver_element(types, locate, el=el)
        logger.debug('滚动页面')
        if index is not None:
            self.driver.execute_script("arguments[0].scrollIntoView();", target[index])
        else:
            self.driver.execute_script("arguments[0].scrollIntoView();", target)

    @property
    def web_current_window(self):

        """
        获取当前窗口句柄 不能单一使用 实际获取的不是当前句柄
        :return:
        """
        current_window = self.driver.current_window_handle
        logger.debug(f'获取当前句柄 {current_window}')
        return current_window

    @property
    def web_all_handle(self):
        """
        获取所有句柄
        :return:  list
        """
        handle = self.driver.window_handles
        logger.debug(f'获取所有句柄 {handle}')
        return handle

    def web_switch_windows(self, index: int) -> EM or None:
        """
        多窗口切换
        :param index: 列表索引 all_handle的列表索引位置
        :return:
        """
        handle = self.web_all_handle[index]

        try:
            logger.debug(f'窗口已经切换{handle}')
            return self.driver.switch_to.window(handle)
        except Exception as e:
            logger.debug("查找窗口句柄handle异常-> {0}".format(e))

    def web_switch_frame(self, types: str, locate: str, index: int = None) -> None:
        """
        #切换到 iframe
        :param types: 定位类型
        :param locate: 定位元素
        :param index: 列表索引位置
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个

        if index is not None:
            el = 'l'
        logger.debug('切换到 iframe')
        if el is not None and index is not None:
            # 多个定位定位 利用index 列表索引点击
            element = self.driver_element(types=types, locate=locate, el=el)[index]
            self.driver.switch_to.frame(element)
        else:
            # 单个定位点击
            element = self.driver_element(types=types, locate=locate)
            self.driver.switch_to.frame(element)

    def web_switch_default_content(self) -> None:
        """
        返回默认节点
        :return:
        """
        logger.debug('返回到默认节点')
        self.driver.switch_to.default_content()

    def web_switch_parent_frame(self) -> None:
        """
        返回父节点
        :return:
        """
        logger.debug('返回父节点')
        self.driver.switch_to.parent_frame()

    def web_switch_to_alert(self) -> EM or None:
        """
        切换焦点到弹框
        """
        try:
            accept = self.driver.switch_to.alert
            logger.debug('切换焦点到弹框')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def web_accept(self) -> EM or None:
        """
        警告框处理 确认
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.accept()
            logger.debug('警告框已确认')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def web_dismiss(self) -> EM or None:
        """
        警告框处理  取消
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.dismiss()
            logger.debug('警告框已取消')
            return accept
        except Exception as e:
            logger.error("查找dismiss弹出框异常-> {0}".format(e))

    def web_alert_text(self) -> None or str:
        """
        警告框处理 提取警告框文本
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.text
            logger.debug(f'警告框文本信息为 {accept}')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def screen_shot(self, doc: Optional[None] = 'app', imgreport: bool = True) -> str or None:
        """
        截取当前界面图片
        :param doc:  str 名称
        :param imgreport:  str 图片追加到测试报告 默认添加到报告
        :return:
        """

        filename = doc + "_" + str(round(time.time() * 1000)) + ".png"
        if len(filename) >= 200:
            filename = str(round(time.time() * 1000)) + ".png"
        filepath = os.path.join(PRPORE_SCREEN_DIR, filename)

        self.driver.save_screenshot(filepath)
        if imgreport:
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=filename,
                          attachment_type=allure.attachment_type.PNG)
        logger.debug(f"截图成功已经存储在: {filepath}")
        return filepath

    def web_get_dropdown_options_count(self, types: str, locate: str) -> str or None:
        """
        获取下拉选项的个数
        :param types: 定位类型
        :param locate: 定位器
        :return:
        """

        element = self.driver_element(types, locate)
        sel = Select(element)
        options = sel.options
        logger.debug(f'获取下拉选项的个数:{options}')
        return options

    def web_element_hover(self, types: str, locate: str) -> EM or None:
        """
        获取元素后悬停到元素位置
        :param types: 定位类型
        :param locate: 定位器
        :return:
        """
        element = self.driver_element(types, locate)
        hover = ActionChains(self.driver).move_to_element(element).perform()
        logger.debug(f"鼠标悬停位置{locate}")
        return hover

    def web_element_hover_clicks(self, types: str, locate: str, index: int = None) -> None:
        """
        获取元素后悬停到元素位置 后点击该元素
        :param types: 定位类型
        :param locate: 定位器
        :param index: 多个时列表索引
        :return:
        """
        element = self.driver_element(types, locate)
        ActionChains(self.driver).move_to_element(element).perform()
        self.sleep(0.5)
        self.often_click(types=types, locate=locate, index=index)
        logger.debug(f"鼠标悬停位置{locate} 点击")

    def web_save_as_img(self, types: str, locate: str, filename: str, sleep: int = 1) -> None or str:
        """
       图片另存为 下载文件也可以直接使用
        :param types: 定位类型
        :param locate: 定位器
        :param filename: 图片名称 路径必须要输入正确 以为函数没办法判断是否成功
        :param sleep: 等待windo 窗口时间 默认 1 秒
        :return: str path 文件路径
        """
        if sys.platform.lower() == 'win32':
            import pyautogui, pyperclip
            # 右键点击
            self.web_right_click(types=types, locate=locate)

            # 图片另存为
            pyautogui.typewrite(['V'])

            # 将地址以及文件名复制
            pic_dir = None
            pyperclip.copy(os.path.join(PRPORE_SCREEN_DIR, f'{filename}.jpg'))
            # 等待窗口打开，以免命令冲突，粘贴失败，试过很多次才有0.8，具体时间自己试
            self.sleep(sleep)
            # 粘贴
            pyautogui.hotkey('ctrlleft', 'V')
            # 保存
            pyautogui.press('enter')
            logger.debug(f'图片路径为{filename}！')
            return pic_dir

    def web_selcet_locat(self, types: str, locate: str, value: str) -> None:
        """
        下拉框操作  **此函数只支持 Select标签 其它标签不支持
        :param types:  定位类型
        :param locate: 定位参数
        :param value:   #选项文字内容
            # 通过index进行选择
            .select_by_index(1)
            # 通过value进行选择
            .select_by_value("2")
            select_by_visible_text("Male")
            # 通过选项文字进行选择
        :return:
        """
        selcet = self.driver_element(types, locate)
        Select(selcet).select_by_visible_text(value)
        logger.debug('web下拉框选择')

    def is_element_var(self, var) -> bool:
        """
        检查值是否存在
        :param var:查询的值
        :param locate: 定位器
        :return:
        """
        content = self.web_html_content
        if var in content:
            return True
        else:
            return False

    def web_is_element_displayed(self, types: str, locate: str) -> EM or None:
        """
        检查元素是否存在
        :param types:定位类型
        :param locate: 定位器
        :return:
        """
        if types and locate is not None:

            element = self.driver_element(types, locate)
            displayed = element.is_displayed()
            if displayed:
                return True
            else:
                return False
        else:
            logger.error('类型定位元素不能为空')

    def web_title_contains(self, text: str) -> bool:
        """
        判断当前页面的title是否包含
        :param text:内容
        :return: bool
        """
        return EC.title_contains(text)(self.driver)

    def web_title_is(self, text: str) -> bool:
        """
        判断当前页面的title是否包含
        :param text:内容
        :return: bool
        """
        return EC.title_is(text)(self.driver)

    def web_presence_of_element_located(self, types: str, locate: str, ) -> bool:
        """
        检查是否加载到dom树
        :param types: 定位类型
        :param locate: 定位元素
        :return: driver 对象
        """
        types = self.get_by_type(types)

        wait = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                             poll_frequency=POLL_FREQUENCY)
        try:
            em = wait.until(EC.presence_of_element_located((types, locate)))
            if em:
                return True
            else:
                return False

        except Exception as e:
            logger.error(e)
            return False

    def web_visibility_of_element_located(self, types: str, locate: str, ) -> bool:
        """
        检查特定元素是否存在于DOM树中并可见
        :param types: 定位类型
        :param locate: 定位元素
        :return: driver 对象
        """
        types = self.get_by_type(types)

        wait = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                             poll_frequency=POLL_FREQUENCY)
        try:
            em = wait.until(EC.visibility_of_element_located((types, locate)))
            if em:
                return True
            else:
                return False

        except Exception as e:
            logger.error(e)
            return False

    def web_element_to_be_clickable(self, types: str, locate: str, ) -> bool or EM:
        """
        检查特定元素是否可点击，如果可以则返回该元素，否则返回False
        :param types: 定位类型
        :param locate: 定位元素
        :return: driver 对象
        """
        types = self.get_by_type(types)

        wait = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                             poll_frequency=POLL_FREQUENCY)
        try:
            em = wait.until(EC.element_to_be_clickable((types, locate)))
            if em:
                return em
        except Exception as e:
            logger.error(e)
            return False

    def web_frame_to_be_available_and_switch_to_it(self, types: str, locate: str, ) -> bool:
        """
        检查窗口是否可被切换，如果是返回True，否则返回False
        :param types: 定位类型
        :param locate: 定位元素
        :return: driver 对象
        """
        types = self.get_by_type(types)

        wait = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                             poll_frequency=POLL_FREQUENCY)
        try:
            em = wait.until(EC.frame_to_be_available_and_switch_to_it((types, locate)))
            return em
        except Exception as e:
            logger.error(e)
            return False

    def web_element_to_be_selected(self, types: str, locate: str, ) -> bool:
        """
        检查特定元素是否被选中，如果是，返回True，否则返回False
        :param types: 定位类型
        :param locate: 定位元素
        :return: driver 对象
        """
        types = self.get_by_type(types)

        wait = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                             poll_frequency=POLL_FREQUENCY)
        try:
            em = wait.until(EC.element_to_be_selected((types, locate)))
            return em
        except Exception as e:
            logger.error(e)
            return False

    def web_send_enter_key(self, types: str, locate: str, index: int = None) -> None:
        """
        发送回车键
        :param types:
        :param locate:
        :param index:
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('回车键操作')
        if el is not None and index is not None:
            # 多个定位
            self.driver_element(types=types, locate=locate, el=el)[index].send_keys(Keys.ENTER)
        else:
            # 单个定位提取文本元素必须是唯一 如果多个时默认返回第一个
            self.driver_element(types=types, locate=locate).send_keys(Keys.ENTER)

    def web_send_down_or_up_key(self, types: str, locate: str, index: int = None, key: str = 'down') -> None:
        """
        按下 键盘 下或者上
        :param types:
        :param locate:
        :param index:
        :param key: down or up
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        logger.debug('键盘上键操作')
        if index is not None:
            el = 'l'

        if key == 'down':
            keys = Keys.DOWN
        else:
            keys = Keys.UP

        if el is not None and index is not None:
            self.driver_element(types=types, locate=locate, el=el)[index].send_keys(keys)
        else:
            self.driver_element(types=types, locate=locate).send_keys(keys)

    def driver_element(self, types: str, locate: str, el: str = None, ) -> EM or None:
        """
        返回 element
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :return: driver 对象
        """
        types = self.get_by_type(types)

        if el is not None:  # find_elements
            element = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                    poll_frequency=POLL_FREQUENCY).until(
                lambda x: x.find_elements(types, locate))
            return element
        else:  # find_element
            element = WebDriverWait(self.driver, timeout=IMPLICITLY_WAIT_TIME,
                                    poll_frequency=POLL_FREQUENCY).until(
                lambda x: x.find_element(types, locate))
            return element

    def web_submit(self, types: str, locate: str, index: int = None) -> None:
        """
        获取元素后  提交 * 前提是input元素的type为submit
        :param types: 定位类型
        :param locate: 定位元素
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('提交操作')
        if el is not None and index is not None:
            # 多个定位定位 利用index 列表索引点击
            self.driver_element(types=types, locate=locate, el=el)[index].submit()
        else:
            # 单个定位点击
            self.driver_element(types=types, locate=locate).submit()

    def web_right_click(self, types: str, locate: str, index: int = None) -> None:
        """
        获取元素后 右键点击
        :param types: 定位类型
        :param locate: 定位元素
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('web右键点击')
        if el is not None and index is not None:
            element = self.driver_element(types=types, locate=locate, el=el)[index].click()
            ActionChains(self.driver).context_click(element).perform()
        else:
            # 单个定位点击
            element = self.driver_element(types=types, locate=locate, ).click()
            ActionChains(self.driver).context_click(element).perform()

    def web_double_click(self, types: str, locate: str, index: int = None) -> None:
        """
        获取元素后 双击击
        :param types: 定位类型
        :param locate: 定位器
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('web双击点击')
        if el is not None and index is not None:
            element = self.driver_element(types=types, locate=locate, el=el)[index]
            ActionChains(self.driver).double_click(element).perform()
        else:
            # 单个定位点击
            element = self.driver_element(types=types, locate=locate)
            ActionChains(self.driver).double_click(element).perform()

    def web_js_clear(self, types: str, locate: str, index: int = None) -> None:
        """
        js方式清除 输入框
        :param types: 定位类型
        :param locate: 定位元素
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('web js清除操作')
        if el is not None and index is not None:
            element = self.driver_element(types=types, locate=locate, el=el)[index]
        else:
            element = self.driver_element(types=types, locate=locate)

        self.driver.execute_script("arguments[0].value = '';", element)

    def web_execute_js(self, js: str) -> None:
        """
        执行js
        :param js: js 语法
        """
        logger.debug('web js执行操作')
        self.driver.execute_script(js)

    def web_jsclear_continue_input(self, types: str, locate: str, text: str, index: int = None) -> None:
        """
        js清除数据在输入
        :param types: 定位类型
        :param locate: 定位元素
        :param text: 输入文本
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        logger.debug('js清除数据在输入')
        self.web_js_clear(types=types, locate=locate, index=index)
        self.sleep(0.5)
        self.often_input(types=types, locate=locate, text=text, index=index)

    def often_text(self, types: str, locate: str, index: int = None) -> None or EM:
        """
        获取元素  提取文本内容
        :param types: 定位类型
        :param locate: 定位元素
        :param index: 列表索引位置  find_element传递时 此值必填
        :return: driver 对象
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('提取文本内容')
        if el is not None and index is not None:
            # 多个定位
            return self.driver_element(types=types, locate=locate, el=el)[index].text
        else:
            # 单个定位提取文本元素必须是唯一 如果多个时默认返回第一个
            return self.driver_element(types=types, locate=locate).text

    def often_click(self, types: str, locate: str, index: int = None) -> None:
        """
        获取元素后  点击
        :param types: 定位类型
        :param locate: 定位元素
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('点击操作')
        if el is not None and index is not None:
            # 多个定位定位 利用index 列表索引点击
            self.driver_element(types=types, locate=locate, el=el)[index].click()
        else:
            # 单个定位点击
            self.driver_element(types=types, locate=locate).click()

    def often_input(self, types: str, locate: str, text: str, index: int = None) -> None:
        """
        获取元素后输入 并支持键盘操作
        :param types: 定位类型
        :param locate:  定位元素或者 表达式
        :param text:  输入内容
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('输入操作')
        if el is not None and index is not None:
            self.driver_element(types=types, locate=locate, el=el)[index].send_keys(text)
        else:
            self.driver_element(types=types, locate=locate, ).send_keys(text)

    def often_clear(self, types: str, locate: str, index: int = None) -> None:
        """
        清除输入框  * 此方法不适用时 请用js_clear
        :param types: 定位类型
        :param locate: 定位元素

        :param index: 列表索引位置  find_element传递时 此值必填
        """
        el = None  # 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        if index is not None:
            el = 'l'
        logger.debug('清除操作')
        if el is not None and index is not None:
            self.driver_element(types=types, locate=locate, el=el)[index].clear()
        else:
            self.driver_element(types=types, locate=locate).clear()

    def often_clear_continue_input(self, types: str, locate: str, text: str, index: int = None) -> None:
        """
        清除数据在输入
        :param types: 定位类型
        :param locate: 定位元素
        :param text: 输入文本
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        logger.debug('清除数据在输入操作')
        self.often_clear(types=types, locate=locate, index=index)
        self.sleep(0.5)
        self.often_input(types=types, locate=locate, text=text, index=index)

    def get_case(self, yaml_names=None, case_names=None):
        """
        获取用例数据   如果 case_names 以 test_ 开头直接找 caseYAML 目录下  如果不是 找 locaotrTAML
        :param yaml_names: ymal 路径
        :param case_names:  用例名称
        :return:
        """
        if yaml_names is not None:
            d = GetCaseYmal(yaml_name=yaml_names, case_name=case_names)
            return d
        else:
            raise ErrorExcep('yaml路径不能为空！')


class Web(Base):
    """
     常用定位方式  id,xpath,link_text/link,partial_link_text/partial,name,
        tag_name/tag,class_name/class,css_selector/css
    """

    def web_judge_execution(self, types, locate, operate=None, text=None, notes=None, index=None, wait=None):
        """
          操作类型:
        操作类型                                    执行动作
        input                       >               输入
        click                       >               点击
        text                        >               提取文本
        submit                      >               提交
        scroll                      >               滑动下拉
        clear                       >               清除
        jsclear                     >               js清除
        jsclear_continue_input      >               js清除后输入
        clear_continue_input        >               清除在输入
        iframe                      >               跳转到iframe
        web_url                     >               获取当前url
        web_title                   >               获取当前title
        web_html_content            >               获取html内容

        判断 operate 执行操作
        :param locate:  表达 或者定位元素
        :param operate: 执行操作
        :param text: 输入文本内容
        :param index: 多个步骤列表索引
        :param wait: 操作等待
        :return:

        """

        if operate not in Operation.web_operation.value:
            logger.error(f'输入的{operate}暂时不支持此操作！！！')
            logger.error(f'目前只支持{Operation.web_operation.value}')
            raise ErrorExcep(f'输入的{operate}暂时不支持此操作！！！')

        if operate is None:
            el = index  # 如果index 为空默认多个
            return self.driver_element(types=types, locate=locate, el=el)

        else:
            if operate == 'input':  # 输入操作
                if text is not None:
                    self.sleep(wait)
                    logger.debug(notes)
                    return self.often_input(types=types, locate=locate, text=text, index=index)
                else:
                    logger.error(' 函数必须传递 text 参数')

            elif operate == 'click':  # 点击操作
                self.sleep(wait)
                logger.debug(notes)
                return self.often_click(types=types, locate=locate, index=index)

            elif operate == 'text':  # 提取文本
                self.sleep(wait)
                logger.debug(notes)
                return self.often_text(types=types, locate=locate, index=index)

            elif operate == 'submit':  # 提交操作
                self.sleep(wait)
                logger.debug(notes)
                return self.web_submit(types=types, locate=locate, index=index)

            elif operate == 'scroll':  # 滚动下拉到指定位置
                self.sleep(wait)
                logger.debug(notes)
                return self.web_scroll_to_ele(types=types, locate=locate, index=index)

            elif operate == 'clear':  # 清除操作
                self.sleep(wait)
                logger.debug(notes)
                return self.often_clear(types=types, locate=locate, index=index)

            elif operate == 'jsclear':  # js清除操作
                self.sleep(wait)
                logger.debug(notes)
                return self.web_js_clear(types=types, locate=locate, index=index)

            elif operate == 'jsclear_continue_input':  # js清除后在输入操作
                if text is not None:
                    self.sleep(wait)
                    logger.debug(notes)
                    return self.web_jsclear_continue_input(types=types, locate=locate, text=text, index=index)
                else:
                    logger.debug(' 函数必须传递 text 参数')

            elif operate == 'clear_continue_input':  # 清除后在输入操作
                if text is not None:
                    self.sleep(wait)
                    return self.often_clear_continue_input(types=types, locate=locate, text=text, index=index)
                else:
                    logger.debug(' 函数必须传递 text 参数')

            elif operate == 'iframe':  # iframe切换   switch_default_content切换最外层 switch_parent_frame切换父节点
                self.sleep(wait)
                logger.debug(notes)
                return self.web_switch_frame(types=types, locate=locate, index=index)

            elif operate == 'web_url':  # 获取当前url  types必须是 function 时
                self.sleep(wait)
                logger.debug(notes)
                return self.web_url

            elif operate == 'web_title':  # 获取当前title必须是 function 时
                self.sleep(wait)
                logger.debug(notes)
                return self.web_title

            elif operate == 'web_html_content':  # 获取当前html信息 操作类型必须是 types必须是 function 时
                self.sleep(wait)
                logger.debug(notes)
                return self.web_html_content

    def webexe(self, yamlfile, case, text=None, wait=0.1):
        """
        自动执行定位步骤
        :param yamlfile:  yaml文件
        :param case: yaml定位用例
        :param text:  输入内容
        :param wait:  等待多少
        :return:
        """
        relust = None  # 断言结果  最后一步才返回

        yaml = replace_py_yaml(yamlfile)

        locator_data = self.get_case(yaml, case)
        locator_step = locator_data.stepCount()

        for locator in range(locator_step):
            waits = locator_data.locawait(locator)
            if locator_data.operate(locator) in ('input', 'clear_continue_input', 'jsclear_continue_input'):
                self.web_judge_execution(types=locator_data.types(locator), locate=locator_data.locate(locator),
                                         operate=locator_data.operate(locator), notes=locator_data.info(locator),
                                         text=text, index=locator_data.listindex(locator))
            else:
                relust = self.web_judge_execution(types=locator_data.types(locator),
                                                  locate=locator_data.locate(locator),
                                                  operate=locator_data.operate(locator),
                                                  notes=locator_data.info(locator),
                                                  index=locator_data.listindex(locator))
            # 等待时间 如果yaml没有就使用默认
            if waits is not None:
                wait = waits

            self.sleep(wait)
        return relust


class AutoRunCase(Web):
    """
    自动执行测试用列
    """

    def run(self, yamlfile, case, test_date=None, forwait=None):
        """
        自动执行定位步骤  使用run 函数时 test_date 直接传递为可迭代对象
        :param yamlfile:  yaml文件
        :param case: yaml定位用例
        :param test_date:  测试数据
        :param forwait:  多步骤循环等待 /s
        :return:
        """

        relust = None

        yaml = replace_py_yaml(yamlfile)

        locator_data = self.get_case(yaml, case)
        test_dict = locator_data.test_data()

        locator_step = locator_data.stepCount()

        for locator in range(locator_step):
            waits = locator_data.locawait(locator)
            if locator_data.operate(locator) in ('input', 'clear_continue_input', 'jsclear_continue_input'):

                self.web_judge_execution(types=locator_data.types(locator), locate=locator_data.locate(locator),
                                         operate=locator_data.operate(locator), notes=locator_data.info(locator),
                                         text=test_date[locator], index=locator_data.listindex(locator),
                                         wait=locator_data.locawait(locator))
            else:
                relust = self.web_judge_execution(types=locator_data.types(locator),
                                                  locate=locator_data.locate(locator),
                                                  operate=locator_data.operate(locator),
                                                  notes=locator_data.info(locator),
                                                  index=locator_data.listindex(locator),
                                                  wait=locator_data.locawait(locator))
            if waits is not None:
                forwait = waits

            self.sleep(forwait)

        # 断言函数
        if ('assertion' and 'assertype') in test_dict[0] and relust:  # 有断言需求并且有实际值才进行断言
            is_assertion(test_date, relust)
        # return relust
