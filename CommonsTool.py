#!/usr/bin/env python
# -*- coding: utf-8 -*

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

def same_flashData(flashdata, flashaip):
    print("正在对比数据")    
    diff_list = []
    for d in flashdata:
        try:
            assert d in flashaip
        except AssertionError:
            print("不一致的值为: {}".format(d))
            diff_list.append(d)
            continue

    if diff_list == []:
        print("数据一致")
    return diff_list

def wait_loading(driver):
    loading = (By.XPATH, '//div[@class="md-popup-box md-fade" and @style="display: none;"]')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(loading))