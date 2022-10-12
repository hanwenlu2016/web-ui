# -*- coding: utf-8 -*-
# @File: appbase.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/3/18  18:16


import time
from typing import TypeVar, Optional, Callable

from appium.webdriver.common.touch_action import TouchAction

from public.common import ErrorExcep, logger, reda_conf
from public.reda_data import replace_py_yaml
from public.web_base import Base, Operation

# 读取配置参数
APP_UI = reda_conf('APP_UI')
POLL_FREQUENCY = APP_UI.get('APP_POLL_FREQUENCY')
IMPLICITLY_WAIT_TIME = APP_UI.get('APP_IMPLICITLY_WAIT_TIME')
PLATFORM = APP_UI.get('APP_PLATFORM')

AM = TypeVar('AM')  # 可以是任何类型。


class AppBase(Base):

    def app_get_size(self) -> AM:
        """
        获取屏幕分辨率
        :return:
        """
        logger.debug('获取屏幕分辨率')
        rect = self.driver.get_window_size()
        return rect['width'], rect['height']

    def app_device_x_get(self) -> AM:
        """
        获取分辨率 宽
        :return:
        """
        logger.debug('获取分辨率宽')
        return self.driver.get_window_size()['width']

    def app_device_y_get(self) -> AM:
        """
       获取分辨率 高
       :return:
       """
        logger.debug('获取分辨率高')
        return self.driver.get_window_size()['height']

    def app_back(self) -> AM:
        """
        返回键
        :param
        :return:
        """
        logger.debug('操作返回键')
        return self.driver.keyevent(4)

    def app_send_keyevent(self, code: str) -> None:
        """
        发送 keyevent 操作  * 可以百度搜索 keyevent键列表
        :param code:  keyevent码
        :return:
        """
        logger.debug('发送 keyevent 操作')
        self.driver.keyevent(code)

    def app_locks(self, s: float) -> None:
        """
        锁定屏幕
        :param s: 锁定的秒数
        :return:
        """
        logger.debug('锁定屏幕')
        self.driver.lock(s)

    def app_install(self, apppath: str) -> None:
        """
        安装app
        :param apppath: app 路径
        :return:
        """
        logger.debug(f'安装app {apppath}')
        self.driver.install_app(apppath)

    def app_delete(self, app: str) -> None:
        """
        删除app
        :param app: app 包名
        :return:
        """
        logger.debug(f'删除app {app}')
        self.driver.remove_app(app)

    def app_is_install(self, app: str) -> None or bool:
        """
        检查app 是否安装
        :param app: app 包名
        :return: True/False
        """
        logger.debug(f'检查app 是否安装 {app}')
        return self.driver.is_app_installed(app)

    def app_tap(self, element: str = None, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        点击app  如果 element x y 都传递 使用element  and vice versa
        :param element：  定位的元素
        :param x: x点
        :param y: y点
        :return:
        """
        logger.debug('点击app')
        act = TouchAction(self.driver)

        act.tap(element=element, x=x, y=y).perform()

    def app_press_s(self, element: str = None, x: Optional[int] = None, y: Optional[int] = None, s: int = 0.1) -> None:
        """
        app按下 指定秒数
        :param element: 定位的元素   如果 element x y 都传递 使用element  and vice versa
        :param x:
        :param y:
        :param s: 默认按下1秒
        :return:
        """
        logger.debug(f'app按下指定秒数{s}')
        pre = TouchAction(self.driver)
        pre.long_press(el=element, x=x, y=y, duration=s * 1000).perform()

    def app_right_to_left_move_to(self, press_el: str = None, press_x: Optional[int] = 0, press_y: Optional[int] = 0,
                                  mo_el: str = None, mo_x: Optional[int] = 0, mo_y: Optional[int] = 0) -> None:
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
        logger.debug('从右到左')
        right_to_left = TouchAction(self.driver)
        (right_to_left
         .press(press_el, x=press_x, y=press_y)
         .wait(1000).move_to(mo_el, x=mo_x, y=mo_y)
         .release().perform())

    def swipe_left(self, swipe_times: int = 1) -> None:
        """
        向左滑动
        :param swipe_times:
        :return:
        """
        logger.debug("向左滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]

        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.8, height * 0.5, width * 0.2, height * 0.5, duration=800)
            time.sleep(0.5)

    def swipe_right(self, swipe_times: int = 1) -> None:
        """
        向右滑动
        :param swipe_times:
        :return:
        """
        logger.debug("向右滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.2, height * 0.5, width * 0.8, height * 0.5)
            time.sleep(0.5)

    def swipe_up(self, swipe_times: int = 1) -> None:
        """
        向上滑动
        :param swipe_times:
        :return:
        """
        logger.debug("向上滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.5, height * 0.2, width * 0.5, height * 0.8)
            time.sleep(0.5)

    def swipe_down(self, swipe_times: int = 1) -> None:
        """
        向下滑动
        :param swipe_times:
        :return:
        """
        logger.debug("向下滑动" + str(swipe_times) + "次")
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        for i in range(0, swipe_times):
            self.driver.swipe(width * 0.5, height * 0.8, width * 0.5, height * 0.2)
            time.sleep(0.5)

    def scroll_page_one_time(self, direction: str = "up", swipe_times: int = 1) -> None:
        """
        屏幕滑动 几次
        :param direction: 方向
            up: 从下往上
            down: 从上往下
            left: 从右往左
            right: 从左往右
        :param swipe_times: 默认1次
        """
        logger.debug(f'屏幕滑动{swipe_times}次')
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

    def android_background_apps(self, s: float) -> None:
        """
        把 app 放到后台
        :param s: 放置几秒
        :return:
        """
        logger.debug('把app放到后台！')
        self.driver.background_app(s)

    def android_add_volume(self, frequency: int = 1) -> None:
        """
        增加声音 ** 可以搜索 keyevent 查询具体参数
        :param frequency: 增加次数 默认一次
        :return:
        """
        logger.debug('增加音量')
        for i in range(0, frequency):
            self.driver.keyevent(24)

    def android_reduce_volume(self, frequency: int = 1) -> None:
        """
        减小声音
        :param frequency: 减小次数 默认一次
        :return:
        """
        logger.debug('增小音量')
        for i in range(0, frequency):
            self.driver.keyevent(25)

    def android_open_notification(self) -> None:
        """
        打开菜单栏
        :return:
        """
        logger.debug('打开菜单栏')
        return self.driver.open_notifications()


class App(AppBase):
    """
     常用定位方式  class(安卓对应 ClassName / iso对应 type) 、 xpath 、 id、
    """

    def get_fdoc(self, function: Callable) -> str:
        """
        获取函数帮助文档
        function 函数名称
        """
        return function.__doc__.replace(' ', '').replace('\n', '').split(':')[0]

    def app_judge_execution(self, types, locate, operate=None, text=None, notes=None, index=None, wait=None):
        """
          app操作类型 执行:
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
        slide                      >              滑动屏幕 (只支持app)

        判断 operate 执行操作
        :param locate:  表达 或者定位元素
        :param operate: 执行操作
        :param text: 输入文本内容
        :param index: 多个步骤列表索引
        :param wait: 操作等待
        :return:

        """
        if operate not in Operation.app_operation.value:
            logger.error(f'输入的{operate}暂时不支持此操作！！！')
            logger.error(f'目前只支持{Operation.app_operation.value}')
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

            elif operate == 'slide':  # 滑动操作
                self.scroll_page_one_time(direction=locate)

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

    def appexe(self, yamlfile, case, text=None, wait=0.1):
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
            this_types = locator_data.types(locator)  # 通用定位类型
            this_locate = locator_data.locate(locator)  # 通用定位器
            this_ios_types = locator_data.ios_types(locator)  # ios定位类型
            this_ios_locate = locator_data.ios_locate(locator)  # ios定位器
            this_android_types = locator_data.android_types(locator)  # android 定位类型
            this_android_locate = locator_data.android_locate(locator)  # android 定位器

            # 如果为安卓  android_types android_locate都有值就选择安卓的类型和操作类型
            # 否则就选择 默认的操作方式和定位类型
            real_types = None
            real_locate = None

            if this_android_types and this_android_locate:
                if PLATFORM.lower() == 'android':
                    real_types = this_android_types
                    real_locate = this_android_locate

            # 如果为ios  iso定位类型 和操作类型都有选择iso 专属类型操作
            # 否则就选择 默认的操作方式和定位类型
            elif this_ios_types and this_ios_locate:
                if PLATFORM.lower() == 'ios':
                    real_types = this_ios_types
                    real_locate = this_ios_locate
            else:
                real_types = this_types
                real_locate = this_locate

            if real_types and real_locate:
                waits = locator_data.locawait(locator)

                if locator_data.operate(locator) in ('input', 'clear_continue_input', 'jsclear_continue_input'):

                    self.app_judge_execution(types=real_types, locate=real_locate,
                                             operate=locator_data.operate(locator), notes=locator_data.info(locator),
                                             text=text, index=locator_data.listindex(locator))
                else:
                    relust = self.app_judge_execution(types=real_types,
                                                      locate=real_locate,
                                                      operate=locator_data.operate(locator),
                                                      notes=locator_data.info(locator),
                                                      index=locator_data.listindex(locator))
                # 等待时间 如果yaml没有就使用默认
                if waits is not None:
                    wait = waits

                self.sleep(wait)

            else:
                logger.error('定位类型 定位器不能为空')
        return relust
