#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from BasePage import BasePage
from CommonsTool import wait_loading


class News_calendar(BasePage):

    def calendar_lxml_parse(self):
        # 解析网页
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        tablelist = soup.select("div.list.container div.md-cell-item-content > div")

        lxmlList = []
        # import pdb; pdb.set_trace()
        for item in tablelist:
            item_dict = {}
            item_dict['pub_time'] = item.select("div.item-one > span")[0].get_text()
            item_dict['star'] = len(item.select("div.item-one > span")) - 1
            item_dict['title'] = item.select("div.item-two > span")[0].get_text()
            item_dict['the_affect'] = item.select("div.item-two > span")[1].get_text()[:2]
            item_dict['previous'] = item.select("div.item-three > span")[0].get_text()[3:-1]
            item_dict['consensus'] = item.select("div.item-three > span")[1].get_text()[4:-1]
            item_dict['actual'] = item.select("div.item-three > span")[2].get_text()[4:-1]
            lxmlList.append(item_dict)

        print("\n")
        print(lxmlList)
        return lxmlList



    def get_calendar_data(self, driver):
        # 打开浏览器
        self.open()
        wait_loading(self.driver)
        # 点击日历
        calendar_loc = (By.XPATH, '//a[contains(text(), "日历")]')
        self.find_element(*calendar_loc).click()
        wait_loading(self.driver)

        bankReportList = self.calendar_lxml_parse()
        print("日历-数据的长度为: {}".format(len(bankReportList)))


        driver.quit()

        return bankReportList

