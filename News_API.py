#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests 
import re
import datetime

def get_flashAPI(channel, max_time=None):
    api_url = "http://114.55.249.227:8080/eddid/flash_list"
    api_flashList = []
    data = {}
    data['channel'] = channel
    if max_time != None:
        data['max_time'] = max_time

    print("正在请求flash_list接口")
    resp = requests.get(api_url, params=data).json()
    for res in resp['data']:
        # print(res['data'])
        if 'content' in res['data'].keys():

            reg = re.compile('<[^>]*>')
            content = reg.sub('',res['data']['content']).replace('\n','')
            # print(content)
            api_flashList.append(content)


        elif [k in ['name', 'country', 'time_period'] for k in resp.keys()]:
            api_flashList.append(res['data']['country'] + res['data']['time_period'] + res['data']['name'])

    # print("**********************************************************")
    print("接口返回数据的条数为 : {}".format(len(api_flashList)))
    strtime = datetime.datetime.strptime(resp['data'][-1]['time'], "%Y-%m-%d %H:%M:%S")
    startTime = (strtime - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    return api_flashList, startTime



def bank_report(category):
    api_url = 'http://114.55.249.227:9000/v2/bank_report'
    data = []
    data['category'] = category

    resp = requests.post(api_url, data=data).json()


    return resp
