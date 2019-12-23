#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from BasePage import BasePage
from CommonsTool import wait_loading


class Bank_Report(BasePage):

    def same_listofdict(self, pagelist, apilist):
        for i in range(len(pagelist)):
            assert pagelist[i]['pub_time'] == datetime.datetime.strptime(apilist[i]['pub_time'],
                                                                         "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            assert pagelist[i]['name'][0] in apilist[i]['name']
            assert pagelist[i]['name'][1] in apilist[i]['name']
            assert (None if pagelist[i]['previous_rating'] == '' else pagelist[i]['previous_rating']) == apilist[i][
                'previous_rating']
            assert (None if pagelist[i]['latest_rating'] == '' else pagelist[i]['latest_rating']) == apilist[i][
                'latest_rating']
            assert (None if pagelist[i]['previous_target_price'] == '' else pagelist[i]['previous_target_price']) == \
                   apilist[i]['previous_target_price']
            assert (None if pagelist[i]['latest_target_price'] == '' else pagelist[i]['latest_target_price']) == \
                   apilist[i]['latest_target_price']
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

    def get_bank_report_hk(self, driver):
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
        add_btn = driver.find_element_by_xpath('//button//div[@class="md-button-content"]')
        self.scrollinto(add_btn)
        wait_loading(driver)
        add_bankReportList = self.bankReport_lxml_parse()
        print("加载更多后投行报告初始长度为: {}".format(len(add_bankReportList)))

        driver.quit()

        return bankReportList, add_bankReportList

    def get_bank_report_us(self, driver):
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

        import pdb; pdb.set_trace()
        # 点击加载更多按钮
        add_btn = driver.find_element_by_xpath('//button//div[@class="md-button-content"]')
        self.scrollinto(add_btn)
        wait_loading(driver)
        add_bankReportList = self.bankReport_lxml_parse()
        print("加载更多后美股-投行报告初始长度为: {}".format(len(add_bankReportList)))

        driver.quit()

        return bankReportList, add_bankReportList

