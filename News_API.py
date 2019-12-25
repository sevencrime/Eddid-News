#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests 
import re
import datetime
import json

headers = {
    'Content-Type' : 'application/json'
}
requests.adapters.DEFAULT_RETRIES = 5


def get_flashAPI(channel, max_time=None):
    api_url = "http://114.55.249.227:8080/eddid/flash_list"
    api_flashList = []
    data = {}
    data['channel'] = channel
    if max_time != None:
        data['max_time'] = max_time

    print("正在请求flash_list接口")
    resp = requests.get(api_url, params=data, headers=headers).json()

    return resp



def bank_report_API(category):
    api_url = 'http://114.55.249.227:9000/v2/bank_report'
    payload = {}
    payload['category'] = category

    resp = requests.post(api_url, data=json.dumps(payload), headers=headers).json()

    return resp['data']['list']

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
    return resp['data']

def calendar_event_API(nowtime):
    api_url = 'http://114.55.249.227:9000/v2/event'
    payload = {
        "date" : nowtime,
        "category" : ["hk", "us", "cj"] #不要"qh"
    }
    resp = requests.post(api_url, data=json.dumps(payload), headers=headers).json()
    return resp['data']


def calendar_holiday_API(nowtime):
    api_url = 'http://114.55.249.227:9000/v2/holiday'
    payload = {
        "date" : nowtime,
        "category" : ["hk", "us", "cj"] #不要"qh"
    }
    resp = requests.post(api_url, data=json.dumps(payload), headers=headers).json()
    return resp['data']



if __name__ == '__main__':
    # bank_report_API(["hk"])
    calendar_data_API(datetime.datetime.now().strftime("%Y%m%d"))