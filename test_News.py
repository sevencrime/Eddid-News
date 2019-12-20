#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from CommonsTool import *
from GET_New_flash import News_Flash
from GET_News_bankReport import Bank_Report
from News_API import *


def test_flash_futures(driver):
    # 快讯-期货
    url = 'https://download.eddidapp.com/page/eddid-news/index.html'
    n = News_Flash(driver, url)   
    flashList, addflashList= n.get_flash_futures()
    flash_api, lasttime = get_flashAPI(channel=-8200)
    diff_list = same_flashData(flashList, flash_api)
    # print("对比不一致的内容有: ", diff_list)
    print("********************************")
    newflash_api, lasttime = get_flashAPI(channel=-8200, max_time = lasttime)
    diff_list = same_flashData(addflashList, flash_api+newflash_api)


def test_flash_HK(driver):
    # 快讯 -港美股
    url = 'https://download.eddidapp.com/page/eddid-news/index.html'
    n = News_Flash(driver, url)   
    flashList, addflashList= n.get_flash_HK()
    flash_api, lasttime = get_flashAPI(channel=3)
    diff_list = same_flashData(flashList, flash_api)
    # print("对比不一致的内容有: ", diff_list)
    print("********************************")
    newflash_api, lasttime = get_flashAPI(channel=3, max_time = lasttime)
    diff_list = same_flashData(addflashList, flash_api+newflash_api)

def test_bankReport_hk(driver):
    url = 'https://download.eddidapp.com/page/eddid-news/index.html'
    br = Bank_Report(driver, url)
    br.get_bank_report_hk()


if __name__ =='__main__':
    pytest.main(["-s", "-v", "test_News.py::test_bankReport_hk"])