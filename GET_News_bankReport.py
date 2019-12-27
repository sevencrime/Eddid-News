#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from BasePage import BasePage
from CommonsTool import wait_loading
from Logging import Logs


class Bank_Report(BasePage):
    log = Logs()

    def same_listofdict(self, pagelist, apilist):
        for i in range(len(pagelist)):
            self.log.debug("i == {}".format(i))
            self.log.debug("pagelist[i] == {}".format(pagelist[i]))
            self.log.debug("apilist[i] == {}".format(apilist[i]))

            allure.attach('页面的数据 : {} \n\n 接口返回的数据 : {}'.format(pagelist[i], apilist[i]), '对比第 {} 条数据'.format(i),allure.attachment_type.TEXT)

            assert pagelist[i]['pub_time'] == datetime.datetime.strptime(apilist[i]['pub_time'],
                                                                         "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            assert pagelist[i]['name'][0] in apilist[i]['name']
            assert pagelist[i]['name'][1] in apilist[i]['name']
            assert pagelist[i]['previous_rating'] == (apilist[i]['previous_rating'] or '')
            assert pagelist[i]['latest_rating'] == (apilist[i]['latest_rating'] or '')
            assert pagelist[i]['previous_target_price'] == (apilist[i]['previous_target_price'] or '')
            assert pagelist[i]['latest_target_price'] == (apilist[i]['latest_target_price'] or '')
            assert pagelist[i]['institution'] == apilist[i]['institution']

    def bankReport_lxml_parse(self):
        # 解析网页
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        tablelist = soup.select("div.list.container  tbody > tr")

        lxmlList = []
        for tr in tablelist:
            trDict = {}
            trDict['pub_time'] = tr.select("td")[0].get_text()
            trDict['name'] = tr.select("td")[1].get_text().split(" ")
            trDict['previous_rating'] = tr.select("td")[2].get_text().replace("  ", "").split("\n\n")[0].replace("\n", "")
            trDict['latest_rating'] = tr.select("td")[2].get_text().replace("  ", "").split("\n\n")[1].replace("\n", "")
            trDict['previous_target_price'] = tr.select("td")[3].get_text().replace("  ", "").split("\n\n")[0].replace("\n", "")
            trDict['latest_target_price'] = tr.select("td")[3].get_text().replace("  ", "").split("\n\n")[1].replace("\n", "")
            trDict['institution'] = tr.select("td")[4].get_text()

            lxmlList.append(trDict)

        return lxmlList

    def get_bank_report_hk(self):
        # 打开浏览器
        self.open()
        wait_loading(self.driver)
        # 点击投行报告
        bankreport_loc = (By.XPATH, '//a[contains(text(), "投行报告")]')
        self.find_element(*bankreport_loc).click()
        wait_loading(self.driver)

        bankReportList = self.bankReport_lxml_parse()
        print("投行报告初始长度为: {}".format(len(bankReportList)))

        # 点击加载更多按钮
        add_btn = self.driver.find_element_by_xpath('//button//div[@class="md-button-content"]')
        # self.scrollinto(add_btn)
        self.script("arguments[0].scrollIntoView();", add_btn)
        ActionChains(self.driver).move_to_element(add_btn).click().perform()
        wait_loading(self.driver)
        add_bankReportList = self.bankReport_lxml_parse()
        print("加载更多后投行报告初始长度为: {}".format(len(add_bankReportList)))

        self.driver.quit()

        self.log.info("页面初始数据flashList为 : {}".format(bankReportList, ))
        self.log.info("页面点击加载更多后的数据addflashList为 : {}".format(add_bankReportList, ))
        return bankReportList, add_bankReportList

    def get_bank_report_us(self):
        # 打开浏览器
        self.open()
        wait_loading(self.driver)
        # 点击投行报告
        bankreport_loc = (By.XPATH, '//a[contains(text(), "投行报告")]')
        self.find_element(*bankreport_loc).click()
        wait_loading(self.driver)

        us_loc = (By.XPATH, '//a[contains(text(), "美股目标价")]')
        self.find_element(*us_loc).click()
        wait_loading(self.driver)

        bankReportList = self.bankReport_lxml_parse()
        print("美股-投行报告初始长度为: {}".format(len(bankReportList)))

        # 点击加载更多按钮
        add_btn = self.driver.find_element_by_xpath('//button//div[@class="md-button-content"]')
        # self.scrollinto(add_btn)
        self.script("arguments[0].scrollIntoView();", add_btn)
        ActionChains(self.driver).move_to_element(add_btn).click().perform()

        wait_loading(self.driver)
        add_bankReportList = self.bankReport_lxml_parse()
        print("加载更多后美股-投行报告初始长度为: {}".format(len(add_bankReportList)))

        self.driver.quit()

        self.log.info("页面初始数据flashList为 : {}".format(bankReportList, ))
        self.log.info("页面点击加载更多后的数据addflashList为 : {}".format(add_bankReportList, ))
        return bankReportList, add_bankReportList

