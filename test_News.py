#!/usr/bin/env python
# -*- coding: utf-8 -*-
from News import News
import pytest

from News_API import *


def test_News_futures():
    # 快讯-期货
    url = 'https://download.eddidapp.com/page/eddid-news/index.html'
    n = News(url)   
    flashList, addflashList= n.get_flash_futures()
    flash_api, lasttime = get_flashAPI(channel=-8200)
    diff_list = n.same_flashData(flashList, flash_api)
    # print("对比不一致的内容有: ", diff_list)
    print("********************************")
    newflash_api, lasttime = get_flashAPI(channel=-8200, max_time = lasttime)
    diff_list = n.same_flashData(addflashList, flash_api+newflash_api)


def test_News_HK():
    # 快讯 -港美股
    url = 'https://download.eddidapp.com/page/eddid-news/index.html'
    n = News(url)   
    flashList, addflashList= n.get_flash_HK()
    flash_api, lasttime = get_flashAPI(channel=3)
    diff_list = n.same_flashData(flashList, flash_api)
    # print("对比不一致的内容有: ", diff_list)
    print("********************************")
    newflash_api, lasttime = get_flashAPI(channel=3, max_time = lasttime)
    diff_list = n.same_flashData(addflashList, flash_api+newflash_api)


if __name__ =='__main__':
    pytest.main(["-s", "-v"])