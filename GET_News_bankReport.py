#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from BasePage import BasePage
from CommonsTool import wait_loading


class Bank_Report(BasePage):

    def get_bank_report_hk(self):
        self.open()
        bankreport_loc = (By.XPATH, '//a[contains(text(), "投行报告")]')
        # 点击投行报告
        self.find_element(*bankreport_loc).click()
        wait_loading(self.driver)

        # 解析网页
        soup = BeautifulSoup(self.driver.page_source,'lxml')
        tablelist = soup.select("div.list.container  tbody > tr")

        bankReportList = []
        for tr in tablelist:
            trDict = {}
            # for td in tr.select("td"):
            #     print(t   d.get_text())
            trDict['pub_time'] = tr.select("td")[0].get_text()
            trDict['name'] = tr.select("td")[1].get_text()
            trDict['previous_rating'] = tr.select("td")[2].get_text().replace("  ", "").split("\n\n")[0].replace("\n", "")
            trDict['latest_rating'] = tr.select("td")[2].get_text().replace("  ", "").split("\n\n")[1].replace("\n", "")
            trDict['previous_target_price'] = tr.select("td")[3].get_text().replace("  ", "").split("\n\n")[0].replace("\n", "")
            trDict['latest_target_price'] = tr.select("td")[3].get_text().replace("  ", "").split("\n\n")[1].replace("\n", "")
            trDict['institution'] = tr.select("td")[4].get_text()

            bankReportList.append(trDict)

        print(bankReportList)

        return bankReportList

