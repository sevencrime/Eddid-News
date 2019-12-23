#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from BasePage import BasePage
from CommonsTool import wait_loading


class News_Flash(BasePage):

    def lxml_parse(self, driver):
        print("解析网页数据")
        soup = BeautifulSoup(driver.page_source,'lxml')
        context = soup.select("div.md-example-child.news p.md-cell-item-title")
        spantitle = soup.select("div.item-one.item-two > span.title")
        flashList = []
        for text in context:
            # print(text.get_text())
            flashList.append(text.get_text())

        for span in spantitle:
            # print(span.get_text())
            flashList.append(span.get_text())       
        return flashList

    def get_flash_futures(self):
        driver = self.driver
        # print(driver.page_source)
        self.open()
        wait_loading(driver)
        flashList = self.lxml_parse(driver)
        print("页面返回的数据条数为 : {}".format(len(flashList)))

        add_btn = driver.find_element_by_xpath('//button//div[@class="md-button-content"]')

        # 点击加载更多按钮
        print("开始点击加载更多按钮")
        self.scrollinto(add_btn)
        # self.script("arguments[0].scrollIntoView();", add_btn)

        addflashList = self.lxml_parse(driver)
        print("点击加载更多按钮后页面返回的数据条数为 : {}".format(len(addflashList)))

        # print("已经要关闭啦!!!!")
        driver.quit()
        
        # import pdb; pdb.set_trace
        return flashList, addflashList


    def get_flash_HK(self):
        print("开始请求资源网站")
        driver = self.driver
        self.open()
        wait_loading(driver)

        # print(driver.page_source)
        self.find_element(*(By.XPATH, '//a[contains(text(), "港美股")]')).click()
        wait_loading(driver)

        flashList = self.lxml_parse(driver)
        print("快讯-港美股页面返回的数据条数为 : {}".format(len(flashList)))

        add_btn = driver.find_element_by_xpath('//button//div[@class="md-button-content"]')
        # 点击加载更多按钮
        print("快讯-港美股点击加载更多按钮")
        self.scrollinto(add_btn)
        # self.script("arguments[0].scrollIntoView();", add_btn)
        wait_loading(driver)

        addflashList = self.lxml_parse(driver)
        print("快讯-港美股点击加载更多按钮后页面返回的数据条数为 : {}".format(len(addflashList)))

        driver.quit()
        
        # import pdb; pdb.set_trace
        return flashList, addflashList



