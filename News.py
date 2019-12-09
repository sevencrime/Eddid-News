#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup  
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options

class News():

    def __init__(self, url):
        self.url = url

    def find_element(self, driver, *loc):
        try:
            # 确保元素是可见的。
            # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(loc))
            
            # WebDriverWait(self.driver, 20).until(
            #     EC.visibility_of_element_located(loc))

            return self.driver.find_element(*loc)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))
            flag = False
            return flag

    def test_News_futures(self):
        print("开始请求资源网站")
        # 建立browsermobproxy服务, 需指定browsermob-proxy, 类似chromedriver
        server = Server("D:/下载/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat")
        server.start()
        # 创建代理
        proxy = server.create_proxy()
        chrome_options = Options()
        # 为chrome启动时设置代理
        chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
        # 静默模式, 不显示浏览器
        # chrome_options.add_argument('headless')

        driver = webdriver.Chrome(
            executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
            chrome_options=chrome_options)

        # driver.set_script_timeout(3)

        # 这设置了要记录的新HAR(HTTP Archive format(HAR文件)，是用来记录浏览器加载网页时所消耗的时间的工具)
        proxy.new_har(ref="HAR啦", options={'captureHeaders': True, 'captureContent': True}, title="标题")
        driver.get(self.url)

        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "暂无数据")]')))

        # self.find_element(driver, (By.XPATH, '//button'))

        # 获取HAR
        # result = proxy.har
        # print(result)
        # print(driver.page_source)

        soup = BeautifulSoup(driver.page_source,'lxml')
        context = soup.select("div.md-example-child.news p.md-cell-item-title")

        for text in context:
            print(text.get_text())


        # 代理需要关闭
        print("已经要关闭啦!!!!")
        server.stop()
        driver.quit()



if __name__ == '__main__':
    url = 'https://download.eddidapp.com/page/eddid-news/index.html'
    n = News(url)
    n.test_News_futures()