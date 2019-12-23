#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from BasePage import BasePage
from CommonsTool import wait_loading


class News_calendar(BasePage):

    def same_data(self, pagelist, apilist):

        the_affect_CHN = {
            'positive' : '利多',
            'negative' : '利空',
            'null' : '影响较小'
        }
        assert len(pagelist) == len(apilist)
        for i in range(len(pagelist)):
            assert pagelist[i]['pub_time'] == apilist[i]['pub_time']
            assert pagelist[i]['star'] == apilist[i]['star']
            assert pagelist[i]['title'] == apilist[i]['country'] + apilist[i]['time_period'] + apilist[i]['indicator_name']
            assert pagelist[i]['the_affect'] == the_affect_CHN[apilist[i]['the_affect']]
            assert pagelist[i]['previous'] == apilist[i]['previous']
            assert (None if '-' in pagelist[i]['consensus'] else pagelist[i]['consensus']) == apilist[i]['consensus']
            assert pagelist[i]['actual'] == apilist[i]['actual']


    def calendar_lxml_parse(self):
        # 解析网页
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        tablelist = soup.select("div.list.container div.md-cell-item-content > div")

        lxmlList = []
        # import pdb; pdb.set_trace()
        for item in tablelist:
            item_dict = {}
            item_dict['pub_time'] = '{} {}'.format(datetime.datetime.now().strftime("%Y-%m-%d"), item.select("div.item-one > span")[0].get_text())
            item_dict['star'] = len(item.select("div.item-one > span")) - 1
            item_dict['title'] = item.select("div.item-two > span")[0].get_text()
            item_dict['the_affect'] = item.select("div.item-two > span")[1].get_text()[:2]
            item_dict['previous'] = item.select("div.item-three > span")[0].get_text()[3:-1].replace(" ", "")
            item_dict['consensus'] = item.select("div.item-three > span")[1].get_text()[4:-1].replace(" ", "")
            item_dict['actual'] = item.select("div.item-three > span")[2].get_text()[4:-1].replace(" ", "")
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

        calendardataList = self.calendar_lxml_parse()
        print("日历-数据的长度为: {}".format(len(calendardataList)))


        driver.quit()

        return calendardataList

