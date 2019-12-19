#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
import requests
import re
from BasePage import BasePage
import datetime


class News(BasePage):

    def __init__(self, url):
        self.url = url

    def same_flashData(self, flashdata, flashaip):
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

    def driver(self):
        chrome_options = Options()
        # 静默模式, 不显示浏览器
        chrome_options.add_argument('headless')

        driver = webdriver.Chrome(
            executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
            chrome_options=chrome_options)

        super(News, self).__init__(driver, self.url)
        # 打开浏览器
        self.open()

        # 等待数据加载
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "暂无数据")]')))

        return driver


    def get_flashAPI(self, max_time=None):
        url = "http://114.55.249.227:8080/eddid/flash_list"
        api_flashList = []
        data = {
            'channel' : -8200, 
        }
        if max_time != None:
            data['max_time'] = max_time

        print("正在请求flash_list接口")
        resp = requests.get(url, params=data).json()
        # print(type(resp))
        # import pdb; pdb.set_trace()
        for res in resp['data']:
            # print(res['data'])
            if 'content' in res['data'].keys():

                reg = re.compile('<[^>]*>')
                content = reg.sub('',res['data']['content']).replace('\n','')
                # print(content)
                api_flashList.append(content)


            elif [k in ['name', 'country', 'time_period'] for k in resp.keys()]:
                # res['data']['country']
                # res['data']['time_period']
                # res['data']['name']
                api_flashList.append(res['data']['country'] + res['data']['time_period'] + res['data']['name'])

        # print("**********************************************************")
        print("接口返回数据的条数为 : {}".format(len(api_flashList)))
        strtime = datetime.datetime.strptime(resp['data'][-1]['time'], "%Y-%m-%d %H:%M:%S")
        startTime = (strtime - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
        return api_flashList, startTime

    def lxml_parse(self, driver):
        print("正在解析网页数据")
        soup = BeautifulSoup(driver.page_source,'lxml')
        context = soup.select("div.md-example-child.news p.md-cell-item-title")
        spantitle = soup.select("div.item-one.item-two > span.title")
        flashList = []
        for text in context:
            # print(text.get_text())
            flashList.append(text.get_text())

        for span in spantitle:
            # print(span.get_text())
            flashList.append(span.get_text())       
        return flashList

    def get_flash_futures(self):
        print("开始请求资源网站")
        driver = self.driver()
        # print(driver.page_source)

        flashList = self.lxml_parse(driver)

        add_btn = driver.find_element_by_xpath('//button')
        # 点击加载更多按钮
        print("点击加载更多按钮")
        self.scrollinto(add_btn)
        # self.script("arguments[0].scrollIntoView();", add_btn)

        loading = (By.XPATH, '//div[@class="md-popup-box md-fade" and @style="display: none;"]')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(loading))

        addflashList = self.lxml_parse(driver)

        print("已经要关闭啦!!!!")
        driver.quit()
        
        # import pdb; pdb.set_trace
        print("flash_list页面返回的条数为 : {}".format(len(flashList)))
        return flashList, addflashList

def test_News_futures():
    url = 'https://download.eddidapp.com/page/eddid-news/index.html'
    n = News(url)   
    print("开始爬取快讯-期货的数据")
    flashList, addflashList= n.get_flash_futures()
    flash_api, lastdata = n.get_flashAPI()
    diff_list = n.same_flashData(flashList, flash_api)
    # print("对比不一致的内容有: ", diff_list)
    print("********************************")
    # strtime = datetime.datetime.strptime(lastdata['time'], "%Y-%m-%d %H:%M:%S")
    # startTime = (strtime - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    newflash_api, lastdata = n.get_flashAPI(lastdata)
    diff_list = n.same_flashData(addflashList, flash_api+newflash_api)

if __name__ == '__main__':
    test_News_futures()
    # a = '[nihasd还是辣就好大的]</b>'
    # print(re.findall(r">(.+)<", a))