#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


    """
    BasePage封装所有页面都公用的方法
    """
    
    # self只实例本身，相较于类Page而言。

    def __init__(self, selenium_driver, base_url, pagetitle):
        self.driver = selenium_driver
        self.base_url = base_url
        self.pagetitle = pagetitle

    # 通过title断言进入的页面是否正确。
    # 使用title获取当前窗口title，检查输入的title是否在当前title中，返回比较结果（True 或 False）
    def on_page(self, pagetitle):
        return pagetitle in self.driver.title

    # 打开页面，并校验页面链接是否加载正确
    # 以单下划线_开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。
    # def _open(self, url, pagetitle):
    #     # 使用get打开访问链接地址
    #     self.driver.get(url)
    #     self.driver.maximize_window()
    #     # 使用assert进行校验，打开的窗口title是否与配置的title一致。调用on_page()方法
    #     assert self.on_page(pagetitle), u"打开开页面失败 %s" % url


    def browser(self, url, pagetitle, num = 0):
        # driver.get 保护罩,防止打开浏览器超时
        try:
            main_win = self.driver.current_window_handle #得到主窗口句柄

            if len(self.driver.window_handles) == 1 : 
                # 如果只有一个窗口, 打开保护罩
                js='window.open("https://www.baidu.com");'
                self.driver.execute_script(js)  #此时焦点在新打开页面
                for handle in self.driver.window_handles:
                    if handle == main_win:  
                        # print('保护罩WIN', handle, '\nMain', main_win)
                        self.driver.switch_to.window(handle)    #切换回主窗口

            self.driver.get(url)
            self.driver.maximize_window()
            assert self.on_page(pagetitle), u"打开开页面失败 %s" % url

        except TimeoutException:
            if num == 3:
                print(TimeoutException)
                raise TimeoutException
            # 关闭当前超时页面
            for handle in self.driver.window_handles:
                if handle != main_win:
                    # 句柄不等于主窗口,即是保护罩界面,则重新调用
                    self.driver.switch_to_window(handle)
                    self.browser(url, pagetitle, num+1)
                else:
                    # 句柄等于主窗口, 关闭窗口
                    print("切换保护罩")
                    self.driver.close()


    # 定义open方法，调用_open()进行打开链接
    def open(self):
        # self._open(self.base_url, self.pagetitle)
        self.browser(self.base_url, self.pagetitle)

    # 重写元素定位方法
    def find_element(self, *loc):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc))
            
            # WebDriverWait(self.driver, 20).until(
            #     EC.visibility_of_element_located(loc))

            return self.driver.find_element(*loc)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))
            flag = False
            return flag

    def find_elements(self, *loc):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc))
            
            return self.driver.find_elements(*loc)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))
            flag = False
            return flag

    # 重写switch_frame方法
    def switch_frame(self, loc):
        return self.driver.switch_to_frame(loc)

    # 定义script方法，用于执行js脚本，范围执行结果
    def script(self, src, loc=None):
        if loc == None:
            self.driver.execute_script(src)
        else:
            self.driver.execute_script(src, loc)

    # 重写定义send_keys方法
    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        try:
            loc = getattr(self, "_%s" % loc)  # getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))

    def scrollinto(self, loc):
        self.script("arguments[0].scrollIntoView();", loc)
        self.script("arguments[0].click();", loc)
