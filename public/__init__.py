# from appium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from time import sleep
#
#
# class Action():
#     def __init__(self):
#         # 驱动配置
#         self.desired_caps = {
#             'platformName': 'android',
#             'deviceName': 'ec4537ec',
#             'appPackage': 'com.jingdong.app.mall',
#             'appActivity': 'main.MainActivity'
#         }
#         self.driver = webdriver.Remote("http://192.168.203.5:4723" + "/wd/hub", self.desired_caps)
#         self.wait = WebDriverWait(self.driver, 10)
#
#     def comments(self):
#         # 点击进入搜索页面
#         search = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/mp')))
#         search.click()
#         # 输入搜索文本
#         box = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/search_box_layout')))
#         box.set_text('99')
#         # 点击搜索按钮
#         button = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/search_btn')))
#         button.click()
#         # 点击进入商品详情
#         view = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/product_list_item')))
#         view.click()
#         # 进入评论详情
#         tab = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/pd_tab3')))
#         tab.click()
#
#     def scroll(self):
#         while True:
#             pass
#             # # 模拟拖动
#             # self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
#             # sleep(SCROLL_SLEEP_TIME)
#
#     def main(self):
#         self.comments()
#         self.scroll()
#
#
# if __name__ == '__main__':
#     action = Action()
#     action.main()
