#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
import requests
import re
from BasePage import BasePage
import datetime


class News(BasePage):

    def __init__(self, url):
        self.url = url

    def same_flashData(self, flashdata, flashaip):
        print("正在对比数据")    
        diff_list = []
        for d in flashdata:
            try:
                assert d in flashaip
            except AssertionError:
                print("不一致的值为: {}".format(d))
                diff_list.append(d)
                continue

        if diff_list == []:
            print("数据一致")
        return diff_list

    def driver(self):
        chrome_options = Options()
        # 静默模式, 不显示浏览器
        chrome_options.add_argument('headless')

        driver = webdriver.Chrome(
            executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
            chrome_options=chrome_options)

        super(News, self).__init__(driver, self.url)
        # 打开浏览器
        self.open()

        # 等待数据加载
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "暂无数据")]')))

        return driver



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
        driver = self.driver()
        # print(driver.page_source)

        flashList = self.lxml_parse(driver)
        print("页面返回的数据条数为 : {}".format(len(flashList)))

        add_btn = driver.find_element_by_xpath('//button')

        # 点击加载更多按钮
        print("开始点击加载更多按钮")
        self.scrollinto(add_btn)
        # self.script("arguments[0].scrollIntoView();", add_btn)

        loading = (By.XPATH, '//div[@class="md-popup-box md-fade" and @style="display: none;"]')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(loading))

        addflashList = self.lxml_parse(driver)
        print("点击加载更多按钮后页面返回的数据条数为 : {}".format(len(addflashList)))

        # print("已经要关闭啦!!!!")
        driver.quit()
        
        # import pdb; pdb.set_trace
        return flashList, addflashList


    def get_flash_HK(self):
        print("开始请求资源网站")
        driver = self.driver()
        # print(driver.page_source)
        self.find_element(*(By.XPATH, '//a[contains(text(), "港美股")]')).click()
        loading = (By.XPATH, '//div[@class="md-popup-box md-fade" and @style="display: none;"]')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(loading))

        flashList = self.lxml_parse(driver)
        print("快讯-港美股页面返回的数据条数为 : {}".format(len(flashList)))

        add_btn = driver.find_element_by_xpath('//button')

        # 点击加载更多按钮
        print("快讯-港美股点击加载更多按钮")
        self.scrollinto(add_btn)
        # self.script("arguments[0].scrollIntoView();", add_btn)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(loading))

        addflashList = self.lxml_parse(driver)
        print("快讯-港美股点击加载更多按钮后页面返回的数据条数为 : {}".format(len(addflashList)))

        driver.quit()
        
        # import pdb; pdb.set_trace
        return flashList, addflashList



if __name__ == '__main__':
    test_News_futures()
    test_News_HK()
