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
            unit = '' if apilist[i]['unit'] == None else apilist[i]['unit'] #接口返回的unit字段(单位)

            assert pagelist[i]['pub_time'] == apilist[i]['pub_time']
            assert pagelist[i]['star'] == apilist[i]['star']
            assert pagelist[i]['title'] == (apilist[i]['country'] + apilist[i]['time_period'] + apilist[i]['indicator_name'])

            if ('' if apilist[i]['previous'] == None else apilist[i]['previous']) != '':
                assert ('' if '--' in pagelist[i]['previous'] else pagelist[i]['previous']) == ('' if apilist[i]['previous'] == None else apilist[i]['previous']) + unit
            else:
                assert ('' if '--' in pagelist[i]['previous'] else pagelist[i]['previous']) == ''

            if ('' if apilist[i]['consensus'] == None else apilist[i]['consensus']) != '':
                assert ('' if '--' in pagelist[i]['consensus'] else pagelist[i]['consensus']) == ('' if apilist[i]['consensus'] == None else apilist[i]['consensus']) + unit
            else:
                assert ('' if '--' in pagelist[i]['consensus'] else pagelist[i]['consensus']) == ''

            if ('' if apilist[i]['actual'] == None else apilist[i]['actual']) != '':
                assert ('' if '--' in pagelist[i]['actual'] else pagelist[i]['actual']) == ('' if apilist[i]['actual'] == None else apilist[i]['actual']) + unit
            else:
                assert ('' if '--' in pagelist[i]['actual'] else pagelist[i]['actual']) == ''

            if pagelist[i]['the_affect'] != "未公布":
                assert pagelist[i]['the_affect'].find(the_affect_CHN['null' if apilist[i]['the_affect'] == None else apilist[i]['the_affect']]) != -1

    def calendar_lxml_parse(self, calendartime):

        print("开始解析网页")
        # 解析网页
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        tablelist = soup.select("div.list.container div.md-cell-item-content > div")
        lxmlList = []
        for item in tablelist:
            item_dict = {}
            item_dict['pub_time'] = '{} {}'.format(datetime.datetime.strptime(calendartime, "%Y%m%d").strftime("%Y-%m-%d"), item.select("div.item-one > span.date")[0].get_text())
            item_dict['star'] = len(item.select("div.item-one > span.stars > i.star.stared"))
            item_dict['title'] = item.select("div.item-two > span")[0].get_text()
            item_dict['the_affect'] = item.select("div.item-two > span")[1].get_text()
            item_dict['previous'] = item.select("div.item-three > span")[0].get_text()[3:].replace(" ", "")
            item_dict['consensus'] = item.select("div.item-three > span")[1].get_text()[4:].replace(" ", "")
            item_dict['actual'] = item.select("div.item-three > span")[2].get_text()[4:].replace(" ", "")
            lxmlList.append(item_dict)

        return lxmlList

    def get_calendar_data(self, calendartime=None):
        # 打开浏览器
        self.open()
        wait_loading(self.driver)
        # 点击日历
        calendar_loc = (By.XPATH, '//a[contains(text(), "日历")]')
        self.find_element(*calendar_loc).click()
        wait_loading(self.driver)

        # 判断是否要选择日期
        if calendartime != None:
            print("点击的日期为 : {} ".format(calendartime))
            active_calendar = self.driver.find_element_by_xpath('//nav[@class="md-tab-bar tab-day"]//div[@class="day-sub" and text()="{time}"]'.format(time=str(int(calendartime[-2:]))))
            self.script("arguments[0].scrollIntoViewIfNeeded();", active_calendar)
            active_calendar.click()
            wait_loading(self.driver)

        calendardataList = self.calendar_lxml_parse(calendartime)
        print("日历-数据的长度为: {}".format(len(calendardataList)))
        print("页面返回的数据为: {}".format(calendardataList))

        self.driver.quit()

        return calendardataList

