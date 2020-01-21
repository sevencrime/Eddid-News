#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from Commons.Logging import Logs

log = Logs()

headers = {
    'Content-Type' : 'application/json',
    'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}
requests.adapters.DEFAULT_RETRIES = 5


def get_flashAPI(channel, max_time=None):
    api_url = "http://114.55.249.227:8080/eddid/flash_list"
    data = {}
    data['channel'] = channel
    if max_time != None:
        data['max_time'] = max_time

    print("正在请求flash_list接口")
    s = requests.session()
    resp = s.get(api_url, params=data, headers=headers, timeout=10).json()

    log.debug("max_time 为 {} 时, 快讯接口返回的数据为: {}".format((max_time or 'nowtime'), resp, ))
    # allure.attach('', '打开的日期:{}'.format((max_time or 'nowtime')), allure.attachment_type.TEXT)

    return resp

# 投行报告接口, 返回全量数据
def bank_report_API(category):
    api_url = 'http://114.55.249.227:9000/v2/bank_report'
    payload = {}
    payload['category'] = category

    resp = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=10).json()

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

    resp = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=10).json()

    log.debug("日历接口返回的数据为: {}".format(resp['data'], ))

    return resp['data']

# 日历 -- 财经事件接口
def calendar_event_API(nowtime):
    api_url = 'http://114.55.249.227:9000/v2/event'
    payload = {
        "date" : nowtime,
        "category" : ["hk", "us", "cj"] #不要"qh"
    }
    resp = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=10).json()

    log.debug("日历--财经事件接口 返回的数据为: {}".format(resp['data'], ))
    return resp['data']

# 日历 -- 假期接口
def calendar_holiday_API(nowtime):
    api_url = 'http://114.55.249.227:9000/v2/holiday'
    payload = {
        "date" : nowtime,
        "category" : ["hk", "us", "cj"] #不要"qh"
    }
    resp = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=10).json()

    log.debug("日历--假期接口 返回的数据为: {}".format(resp['data'], ))
    return resp['data']



if __name__ == '__main__':
    # bank_report_API(["hk"])
    import time
    start = time.time()
    r = get_flashAPI(-8200)
    print(time.time() - start)
    print(len(r['data']))