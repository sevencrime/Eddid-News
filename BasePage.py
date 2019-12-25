#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class BasePage:
    """
    BasePage封装所有页面都公用的方法
    """
    
    # self只实例本身，相较于类Page而言。
    def __init__(self, selenium_driver, base_url):
        self.driver = selenium_driver
        self.base_url = base_url

    def browser(self, url, num = 0):
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
            # assert self.on_page(pagetitle), u"打开开页面失败 %s" % url

        except TimeoutException:
            if num == 3:
                print(TimeoutException)
                raise TimeoutException
            # 关闭当前超时页面
            for handle in self.driver.window_handles:
                if handle != main_win:
                    # 句柄不等于主窗口,即是保护罩界面,则重新调用
                    self.driver.switch_to_window(handle)
                    self.browser(url, num+1)
                else:
                    # 句柄等于主窗口, 关闭窗口
                    print("切换保护罩")
                    self.driver.close()


    # 定义open方法，调用_open()进行打开链接
    def open(self):
        # self._open(self.base_url, self.pagetitle)
        self.browser(self.base_url)

    # 重写元素定位方法
    def find_element(self, *loc):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc))
            
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
        '''

        :param loc: element
        :param opt_center:  一个 Boolean 类型的值，默认为true:
                            如果为true，则元素将在其所在滚动区的可视区域中居中对齐。
                            如果为false，则元素将与其所在滚动区的可视区域最近的边缘对齐。 根据可见区域最靠近元素的哪个边缘，元素的顶部将与可见区域的顶部边缘对准，或者元素的底部边缘将与可见区域的底部边缘对准。
        :return:
        '''
        # self.script("arguments[0].scrollIntoView();", loc)
        # Element.scrollIntoViewIfNeeded（）方法用来将不在浏览器窗口的可见区域内的元素滚动到浏览器窗口的可见区域。 如果该元素已经在浏览器窗口的可见区域内，则不会发生滚动。 此方法是标准的Element.scrollIntoView()方法的专有变体。
        self.script("arguments[0].scrollIntoViewIfNeeded();", loc)
        self.script("arguments[0].click();", loc)
