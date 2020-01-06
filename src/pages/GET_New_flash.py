#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import allure
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from src.Commons.BasePage import BasePage
from src.Commons.CommonsTool import wait_loading
from src.Commons.Logging import Logs


class News_Flash(BasePage):

    log = Logs()

    def same_flashData(self, pagelist, apilist):
        print("正在对比数据")

        allure.attach('', 'pagelist的长度为 {}'.format(len(pagelist)), allure.attachment_type.TEXT)
        allure.attach('', 'apilist的长度为 {}'.format(len(apilist)), allure.attachment_type.TEXT)
        assert len(pagelist) == len(apilist)
        reg = re.compile('<[^>]*>')
        for i in range(len(pagelist)):
            self.log.debug("i == {}".format(i))
            self.log.debug("pagelist[i] == {}".format(pagelist[i]))
            self.log.debug("apilist[i] == {}".format(apilist[i]))

            allure.attach('页面的数据 : {} \n\n 接口返回的数据 : {}'.format(pagelist[i], apilist[i]), '对比第 {} 条数据'.format(i), allure.attachment_type.TEXT)


            assert pagelist[i]['time'] == apilist[i]['time'][11:]

            try:
                assert pagelist[i]['content'] == reg.sub('', apilist[i]['data']['content']).replace('\n', '')
            except KeyError:
                assert pagelist[i]['content'] == apilist[i]['data']['country'] + apilist[i]['data']['time_period'] + apilist[i]['data']['name']

            try:
                # previous : 前值
                assert pagelist[i]['previous'] == apilist[i]['data']['previous'] + (apilist[i]['data']['unit'] or '')

                # consensus : 预测值
                if apilist[i]['data']['consensus'] == None:
                    assert pagelist[i]['consensus'] == '- -'
                else:
                    assert pagelist[i]['consensus'] == apilist[i]['data']['consensus'] + (apilist[i]['data']['unit'] or '')

                # actual : 公布值
                assert pagelist[i]['actual'] == str(apilist[i]['data']['actual']) + (apilist[i]['data']['unit'] or '')
                assert pagelist[i]['start'] == apilist[i]['data']['start']
            except KeyError:
                continue

            try:
                # 利空利多
                if apilist[i]['data']['affect'] == 0:
                    if pagelist[i]['actual'] > (pagelist[i]['consensus'] or pagelist[i]['previous']):
                        assert pagelist[i]['affect'] == '利多'
                    elif pagelist[i]['actual'] < (pagelist[i]['consensus'] or pagelist[i]['previous']):
                        assert pagelist[i]['affect'] == '利空'

                elif apilist[i]['data']['affect'] == 1:
                    if pagelist[i]['actual'] < (pagelist[i]['consensus'] or pagelist[i]['previous']):
                        assert pagelist[i]['affect'] == '利多'
                    elif pagelist[i]['actual'] > (pagelist[i]['consensus'] or pagelist[i]['previous']):
                        assert pagelist[i]['affect'] == '利空'

            except KeyError:
                continue

    def lxml_parse(self, driver):
        print("解析网页数据")
        soup = BeautifulSoup(driver.page_source,'lxml')
        pagetext = soup.select("div.md-example-child.news div.md-cell-item-content")
        flashList = []
        for page in pagetext:
            item_dict = {}
            if page.select("p.md-cell-item-brief") != [] or page.select("p.md-cell-item-title") != []:
                item_dict['time'] = page.select("p.md-cell-item-brief")[0].get_text()
                item_dict['content'] = page.select("p.md-cell-item-title")[0].get_text()
            else:
                item_dict['time'] = page.select("div.calendar-content > span.time")[0].get_text()
                item_dict['content'] = page.select("div.calendar-content span.title")[0].get_text()
                item_dict['previous'] = page.select("div.calendar-content span.previous")[0].get_text()[3:]
                item_dict['consensus'] = page.select("div.calendar-content span.consensus")[0].get_text()[4:]
                item_dict['actual'] = page.select("div.calendar-content span.actual")[0].get_text()[4:]
                item_dict['start'] = len(page.select("div.calendar-content i.star.stared"))
                item_dict['affect'] = page.select("div.calendar-content span.status")[0].get_text()[:2]

            # print(item_dict)
            flashList.append(item_dict)

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
        wait_loading(driver)

        addflashList = self.lxml_parse(driver)
        print("点击加载更多按钮后页面返回的数据条数为 : {}".format(len(addflashList)))
        # print("已经要关闭啦!!!!")
        driver.quit()

        self.log.debug("页面初始数据flashList为 : {}".format(flashList, ))
        self.log.debug("页面点击加载更多后的数据addflashList为 : {}".format(addflashList, ))

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
        add_btn = driver.find_element_by_xpath('//button//div[@class="md-button-inner"]')
        # 点击加载更多按钮
        print("快讯-港美股点击加载更多按钮")

        # 直接点击和使用arguments[0].click()无法点击, 故使用ActionChains, 但需要element先出现在页面上
        self.script("arguments[0].scrollIntoView();", add_btn)
        ActionChains(self.driver).move_to_element(add_btn).click().perform()

        wait_loading(driver)

        addflashList = self.lxml_parse(driver)
        print("快讯-港美股点击加载更多按钮后页面返回的数据条数为 : {}".format(len(addflashList)))
        driver.quit()
        
        self.log.debug("页面初始数据flashList为 : {}".format(flashList, ))
        self.log.debug("页面点击加载更多后的数据addflashList为 : {}".format(addflashList, ))
        # import pdb; pdb.set_trace
        return flashList, addflashList



