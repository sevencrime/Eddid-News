#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

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

# 日历-数据-当天
def test_calendar_date(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now().strftime("%Y%m%d")
    # 爬页面
    calendardataList = calendar.get_calendar_data()
    # 调用接口
    dataAPI_list = calendar_data_API(nowtime)
    print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_data(calendardataList, dataAPI_list)

# 日历-数据-以前日期
def test_calendar_before(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now()
    # startTime = (nowtime - datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
    # 暂时写死, 不能滑动
    startTime = (nowtime - datetime.timedelta(days=2)).strftime("%Y%m%d")
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartime=startTime)
    # 调用接口
    dataAPI_list = calendar_data_API(startTime)
    print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_data(calendardataList, dataAPI_list)

# 日历-数据-未来日期
def test_calendar_after(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now()
    startTime = (nowtime + datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
    print("对比的日期为 : {}".format(startTime))
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartime=startTime)
    # 调用接口
    dataAPI_list = calendar_data_API(startTime)
    # print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_data(calendardataList, dataAPI_list)


# 日历-财经事件-当天
def test_calendar_event_date(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now().strftime("%Y%m%d")
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartab="财经事件")
    # 调用接口
    dataAPI_list = calendar_event_API(nowtime)
    print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_event(calendardataList, dataAPI_list)

# 日历-财经事件-以前日期
def test_calendar_event_before(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now().strftime("%Y%m%d")
    # startTime = (nowtime - datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
    # 暂时写死, 不能滑动
    startTime = (nowtime - datetime.timedelta(days=2)).strftime("%Y%m%d")
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartab="财经事件", calendartime=startTime)
    # 调用接口
    dataAPI_list = calendar_event_API(startTime)
    print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_event(calendardataList, dataAPI_list)

# 日历-财经事件-未来日期
def test_calendar_event_after(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now()
    startTime = (nowtime + datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
    print("对比的日期为 : {}".format(startTime))
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartab="财经事件", calendartime=startTime)
    # 调用接口
    dataAPI_list = calendar_event_API(startTime)
    # print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_event(calendardataList, dataAPI_list)

# 日历-美港财报-当天
def test_calendar_stock_date(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now().strftime("%Y%m%d")
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartab="美港财报")
    # 调用接口
    dataAPI_list = calendar_data_API(nowtime, stock=True)
    print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_data(calendardataList, dataAPI_list, stock=True)

# 日历-美港财报-以前日期
def test_calendar_stock_before(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now()
    # startTime = (nowtime - datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
    # 暂时写死, 不能滑动
    startTime = (nowtime - datetime.timedelta(days=2)).strftime("%Y%m%d")
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartab="美港财报", calendartime=startTime)
    # 调用接口
    dataAPI_list = calendar_data_API(startTime, stock=True)
    print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_data(calendardataList, dataAPI_list, stock=True)

# 日历-美港财报-未来日期
def test_calendar_stock_after(driver):
    calendar = News_calendar(driver, url)

    nowtime = datetime.datetime.now()
    startTime = (nowtime + datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
    print("对比的日期为 : {}".format(startTime))
    # 爬页面
    calendardataList = calendar.get_calendar_data(calendartab="美港财报", calendartime=startTime)
    # 调用接口
    dataAPI_list = calendar_data_API(startTime, stock=True)
    # print("接口返回的数据为: {}".format(dataAPI_list))
    calendar.same_data(calendardataList, dataAPI_list, stock=True)




if __name__ =='__main__':
    pytest.main(["-s", "-v", "--pdb", "test_News.py::test_calendar_stock_after"])