#!/usr/bin/env python
# -*- coding: utf-8 -*
import datetime

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

def same_listofdict(pagelist, apilist):
    for i in range(len(pagelist)):
        assert pagelist[i]['pub_time'] == datetime.datetime.strptime(apilist[i]['pub_time'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        assert pagelist[i]['name'][0] in apilist[i]['name']
        assert pagelist[i]['name'][1] in apilist[i]['name']
        assert (None if pagelist[i]['previous_rating'] == '' else pagelist[i]['previous_rating']) == apilist[i]['previous_rating']
        assert (None if pagelist[i]['latest_rating'] == '' else pagelist[i]['latest_rating']) == apilist[i]['latest_rating']
        assert (None if pagelist[i]['previous_target_price'] == '' else pagelist[i]['previous_target_price']) == apilist[i]['previous_target_price']
        assert (None if pagelist[i]['latest_target_price'] == '' else pagelist[i]['latest_target_price']) == apilist[i]['latest_target_price']
        assert pagelist[i]['institution'] == apilist[i]['institution']



def wait_loading(driver):
    loading = (By.XPATH, '//div[@class="md-popup-box md-fade" and @style="display: none;"]')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(loading))

