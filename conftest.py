#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from CommonsTool import wait_loading


@pytest.fixture
def driver():
    chrome_options = Options()
    # 静默模式, 不显示浏览器
    chrome_options.add_argument('headless')

    driver = webdriver.Chrome(
        executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
        chrome_options=chrome_options)

    # wait_loading(driver)

    return driver
