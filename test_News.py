#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from GET_New_flash import News_Flash
from GET_News_bankReport import Bank_Report
from GET_News_calendar import News_calendar
from News_API import *

# 生产环境
# url = 'https://download.eddidapp.com/page/eddid-news/index.html'
# uat环境
url = 'https://download.eddidapp.com/page/eddid-news-dev/index.html'

def test_flash_futures(driver):
    # 快讯-期货
    n = News_Flash(driver, url)   
    flashList, addflashList= n.get_flash_futures()
    flash_api, lasttime = get_flashAPI(channel=-8200)
    diff_list = n.same_flashData(flashList, flash_api)
    # print("对比不一致的内容有: ", diff_list)
    print("********************************")
    newflash_api, lasttime = get_flashAPI(channel=-8200, max_time = lasttime)
    diff_list = n.same_flashData(addflashList, flash_api+newflash_api)


def test_flash_HK(driver):
    # 快讯 -港美股
    n = News_Flash(driver, url)   
    flashList, addflashList= n.get_flash_HK()
    flash_api, lasttime = get_flashAPI(channel=3)
    diff_list = n.same_flashData(flashList, flash_api)
    # print("对比不一致的内容有: ", diff_list)
    print("********************************")
    newflash_api, lasttime = get_flashAPI(channel=3, max_time = lasttime)
    diff_list = n.same_flashData(addflashList, flash_api+newflash_api)

def test_bankReport_hk(driver):
    # 实例化
    br = Bank_Report(driver, url)
    # 开始获取投行报告页面的数据
    bankReportList, add_bankReportList = br.get_bank_report_hk()
    # 请求投行报告接口, 返回全部数据
    API_bankReportlist = bank_report_API(category=["hk"])
    # 对比数据
    br.same_listofdict(bankReportList, API_bankReportlist)
    br.same_listofdict(add_bankReportList, API_bankReportlist)

def test_bankReport_us(driver):
    # 实例化
    br = Bank_Report(driver, url)
    # 开始获取投行报告页面的数据
    bankReportList, add_bankReportList = br.get_bank_report_us()
    # 请求投行报告接口, 返回全部数据
    API_bankReportlist = bank_report_API(category=["us"])
    # 对比数据
    br.same_listofdict(bankReportList, API_bankReportlist)
    br.same_listofdict(add_bankReportList, API_bankReportlist)


def test_calendar_date(driver):
    calendar = News_calendar(driver, url)

    calendardataList = calendar.get_calendar_data(driver)
    dataAPI_list = calendar_data_API(datetime.datetime.now().strftime("%Y%m%d"))
    calendar.same_data(calendardataList, dataAPI_list)


if __name__ =='__main__':
    pytest.main(["-s", "-v", "--pdb", "test_News.py::test_calendar_date"])