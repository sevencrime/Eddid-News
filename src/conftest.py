#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from Commons.GlobalMap import GlobalMap
import platform

gm = GlobalMap()

@pytest.fixture
def driver():
    chrome_options = Options()
    # 静默模式, 不显示浏览器
    chrome_options.add_argument('headless')
    # https 设置
    chrome_options.add_argument('--ignore-certificate-errors')
    # 设置窗口大小为iPhone X
    mobileEmulation = {'deviceName': 'iPhone X'}
    chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)

    if platform.system() == "Windows" : 
        driver = webdriver.Chrome(
            executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
            chrome_options=chrome_options)

    elif platform.system() == "Linux" or platform.system() == "linux":
        # 使用远程服务器启动
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:12777/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
            options=chrome_options
        )


    return driver


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    '''
    捕获测试用例结果
    :param item:
    :param call:
    :return:
    '''
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == 'call':
        errlist = set(gm.get_value("errfunc"))

        if rep.failed:
            # 把测试失败的记录下来
            errlist.add(item)

            gm.set_List("errfunc", list(errlist))

        elif rep.passed:
            if item in errlist:
                errlist.remove(item)

            gm.set_List("errfunc", list(errlist))