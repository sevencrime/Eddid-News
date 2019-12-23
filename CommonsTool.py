#!/usr/bin/env python
# -*- coding: utf-8 -*
import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By




def wait_loading(driver):
    loading = (By.XPATH, '//div[@class="md-popup-box md-fade" and @style="display: none;"]')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(loading))

