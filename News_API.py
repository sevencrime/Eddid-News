#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allure
import requests
import re
import datetime
import json

from Logging import Logs

headers = {
    'Content-Type' : 'application/json'
}
requests.adapters.DEFAULT_RETRIES = 5

log = Logs()

def get_flashAPI(channel, max_time=None):
    api_url = "http://114.55.249.227:8080/eddid/flash_list"
    api_flashList = []
    data = {}
    data['channel'] = channel
    if max_time != None:
        data['max_time'] = max_time

    print("正在请求flash_list接口")
    resp = requests.get(api_url, params=data, headers=headers).json()

    log.debug("max_time 为 {} 时, 快讯接口返回的数据为: {}".format((max_time or 'nowtime'), resp, ))
    allure.attach('', '打开的日期:{}'.format((max_time or 'nowtime')), allure.attachment_type.TEXT)

    return resp

# 投行报告接口, 返回全量数据
def bank_report_API(category):
    api_url = 'http://114.55.249.227:9000/v2/bank_report'
    payload = {}
    payload['category'] = category

    resp = requests.post(api_url, data=json.dumps(payload), headers=headers).json()

    log.debug("投行报告接口返回的数据为: {}".format(resp['data']['list'], ))
    return resp['data']['list']

# 日历-数据, 日历-美港财报接口
def calendar_data_API(nowtime, stock=False):
    api_url = 'http://114.55.249.227:9000/v2/data'
    payload = {
        "date" : nowtime,
        "category" : ["hk", "us", "cj"] #不要"qh"
    }
    if stock:
        # 美港财报
        payload['data_type'] = "stock"

    resp = requests.post(api_url, data=json.dumps(payload), headers=headers).json()

    log.debug("日历接口返回的数据为: {}".format(resp['data'], ))


    for i in range(len(resp['data'])):
        allure.attach('{}'.format(resp['data'][i]), '接口返回的第 {} 条数据'.format(i), allure.attachment_type.TEXT)

    return resp['data']

# 日历 -- 财经事件接口
def calendar_event_API(nowtime):
    api_url = 'http://114.55.249.227:9000/v2/event'
    payload = {
        "date" : nowtime,
        "category" : ["hk", "us", "cj"] #不要"qh"
    }
    resp = requests.post(api_url, data=json.dumps(payload), headers=headers).json()

    log.debug("日历--财经事件接口 返回的数据为: {}".format(resp['data'], ))
    return resp['data']

# 日历 -- 假期接口
def calendar_holiday_API(nowtime):
    api_url = 'http://114.55.249.227:9000/v2/holiday'
    payload = {
        "date" : nowtime,
        "category" : ["hk", "us", "cj"] #不要"qh"
    }
    resp = requests.post(api_url, data=json.dumps(payload), headers=headers).json()

    log.debug("日历--假期接口 返回的数据为: {}".format(resp['data'], ))
    return resp['data']



if __name__ == '__main__':
    # bank_report_API(["hk"])
    calendar_data_API(datetime.datetime.now().strftime("%Y%m%d"))