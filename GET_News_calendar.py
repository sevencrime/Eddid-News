#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from BasePage import BasePage
from CommonsTool import wait_loading


class News_calendar(BasePage):

    def same_data(self, pagelist, apilist, stock=False):

        the_affect_CHN = {
            'positive' : '利多',
            'negative' : '利空',
            'null' : '影响较小'
        }
        assert len(pagelist) == len(apilist)
        if not stock:
            for i in range(len(pagelist)):
                unit = '' if apilist[i]['unit'] == None else apilist[i]['unit'] #接口返回的unit字段(单位)
                assert pagelist[i]['star'] == apilist[i]['star']

                assert pagelist[i]['pub_time'] == apilist[i]['pub_time']

                assert pagelist[i]['title'] == (apilist[i]['country'] + apilist[i]['time_period'] + apilist[i]['indicator_name'])

                # 前值
                if (apilist[i]['previous'] or '') != '':
                    assert pagelist[i]['previous'] == apilist[i]['previous'] + unit
                else:
                    assert ('' if '--' in pagelist[i]['previous'] else pagelist[i]['previous']) == ''

                # 预测值
                if (apilist[i]['consensus'] or '') != '':
                    assert pagelist[i]['consensus'] == apilist[i]['consensus'] + unit
                else:
                    assert ('' if '--' in pagelist[i]['consensus'] else pagelist[i]['consensus']) == ''

                # 公布值
                if (apilist[i]['actual'] or '') != '':
                    assert pagelist[i]['actual'] == apilist[i]['actual'] + unit
                else:
                    assert ('' if '--' in pagelist[i]['actual'] else pagelist[i]['actual']) == ''

                if pagelist[i]['the_affect'] != "未公布":
                    assert pagelist[i]['the_affect'] == the_affect_CHN[apilist[i]['the_affect']]

        elif stock:
            for i in range(len(pagelist)):
                unit = '' if apilist[i]['unit'] == None else apilist[i]['unit']  # 接口返回的unit字段(单位)
                assert pagelist[i]['star'] == apilist[i]['star']

                assert pagelist[i]['pub_time'] == apilist[i]['time_status']

                assert pagelist[i]['title'] == (apilist[i]['indicator_name'] + apilist[i]['time_period'])

                if (apilist[i]['previous'] or '') != '':
                    assert pagelist[i]['previous'] == unit + apilist[i]['previous']
                else:
                    assert ('' if '--' in pagelist[i]['previous'] else pagelist[i]['previous']) == ''

                if (apilist[i]['consensus'] or '') != '':
                    assert pagelist[i]['consensus'] == unit + apilist[i]['consensus']
                else:
                    assert ('' if '--' in pagelist[i]['consensus'] else pagelist[i]['consensus']) == ''

                if (apilist[i]['actual'] or '') != '':
                    assert pagelist[i]['actual'] == unit + apilist[i]['actual']
                else:
                    assert ('' if '--' in pagelist[i]['actual'] else pagelist[i]['actual']) == ''

                if pagelist[i]['the_affect'] != "未公布":
                    assert pagelist[i]['the_affect'] == the_affect_CHN[apilist[i]['the_affect']]


    def same_event(self, pagelist, apilist):
        assert len(pagelist) == len(apilist)
        for i in range(len(pagelist)):
            assert pagelist[i]['time_status'] == ('' if apilist[i]['time_status'] == None else apilist[i]['time_status'])
            assert pagelist[i]['event_time'] == apilist[i]['event_time']
            assert pagelist[i]['star'] == apilist[i]['star']
            assert pagelist[i]['event_content'] == apilist[i]['event_content']

    def same_holiday(self, pagelist, apilist):
        assert len(pagelist) == len(apilist)
        for i in range(len(pagelist)):
            assert pagelist[i]['name'] == apilist[i]['country'] + '/' + apilist[i]['name']
            assert pagelist[i]['title'] == apilist[i]['exchange_name'] + apilist[i]['rest_note']

    def calendar_lxml_parse(self, calendartime, calendartab="数据"):

        print("开始解析网页")
        # 解析网页
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        tablelist = soup.select("div.list.container div.md-cell-item-content > div")
        lxmlList = []
        if calendartab == "数据" or calendartab == "美港财报":
            # 日历-数据
            for item in tablelist:
                item_dict = {}
                if calendartab == "数据":
                    item_dict['pub_time'] = '{} {}'.format(datetime.datetime.strptime(calendartime, "%Y%m%d").strftime("%Y-%m-%d"), item.select("div.item-one > span.date")[0].get_text())
                elif calendartab == "美港财报":
                    item_dict['pub_time'] = item.select("div.item-one > span.date")[0].get_text()

                item_dict['star'] = len(item.select("div.item-one > span.stars > i.star.stared"))
                item_dict['title'] = item.select("div.item-two > span")[0].get_text()
                if calendartab == "数据":
                    if item.select("div.item-two > span")[1].get_text() != "未公布":
                        item_dict['the_affect'] = item.select("div.item-two > span")[1].get_text()[:2]
                    else:
                        item_dict['the_affect'] = item.select("div.item-two > span")[1].get_text()

                elif calendartab == "美港财报":
                    if item.select("div.item-two > span")[1].get_text() == "利多股票" or item.select("div.item-two > span")[1].get_text() == "利空股票":
                        item_dict['the_affect'] = item.select("div.item-two > span")[1].get_text()[:2]

                item_dict['previous'] = item.select("div.item-three > span")[0].get_text()[3:].replace(" ", "")
                item_dict['consensus'] = item.select("div.item-three > span")[1].get_text()[4:].replace(" ", "")
                item_dict['actual'] = item.select("div.item-three > span")[2].get_text()[4:].replace(" ", "")
                lxmlList.append(item_dict)

        elif calendartab == "财经事件":
            for item in tablelist:
                item_dict = {}
                # 发布时间状态
                item_dict['time_status'] = item.select("div.item-one > span")[0].get_text()
                # 事件时间
                item_dict['event_time'] = '{} {}'.format(datetime.datetime.strptime(calendartime, "%Y%m%d").strftime("%Y-%m-%d"), item.select("div.item-one > span")[1].get_text())
                # 星级
                item_dict['star'] = len(item.select("div.item-one > span.stars > i.star.stared"))
                # event_content
                item_dict['event_content'] = item.select("div.item-two > span")[0].get_text()

                lxmlList.append(item_dict)

        elif calendartab == "假期" :
            for item in tablelist:
                item_dict = {}
                item_dict['name'] = item.select("div.item-one > span")[0].get_text()
                item_dict['title'] = item.select("div.item-two > span")[0].get_text()
                lxmlList.append(item_dict)

        return lxmlList

    def get_calendar_data(self, calendartime=None, calendartab="数据"):
        # 打开浏览器
        self.open()
        wait_loading(self.driver)
        # 点击日历
        calendar_loc = (By.XPATH, '//a[contains(text(), "日历")]')
        self.find_element(*calendar_loc).click()
        wait_loading(self.driver)

        if calendartab == "财经事件":
            tab_loc = (By.XPATH, '//a[contains(text(), "财经事件")]')
            self.find_element(*tab_loc).click()
            wait_loading(self.driver)
        elif calendartab == "美港财报":
            tab_loc = (By.XPATH, '//a[contains(text(), "美港财报")]')
            self.find_element(*tab_loc).click()
            wait_loading(self.driver)
        elif calendartab == "假期":
            tab_loc = (By.XPATH, '//a[contains(text(), "假期")]')
            self.find_element(*tab_loc).click()
            wait_loading(self.driver)

        # 判断是否要选择日期
        if calendartime != None:
            print("点击的日期为 : {} ".format(calendartime))
            active_calendar = self.driver.find_element_by_xpath('//nav[@class="md-tab-bar tab-day"]//div[@class="day-sub" and text()="{time}"]'.format(time=str(int(calendartime[-2:]))))
            self.script("arguments[0].scrollIntoViewIfNeeded();", active_calendar)
            active_calendar.click()
            wait_loading(self.driver)

        calendardataList = self.calendar_lxml_parse(calendartime, calendartab)
        print("数据的长度为: {}".format(len(calendardataList)))
        print("页面返回的数据为: {}".format(calendardataList))

        self.driver.quit()

        return calendardataList

