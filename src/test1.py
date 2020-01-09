from time import sleep

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pytest

driver = webdriver.Remote(
command_executor='http://192.168.50.158:4444/wd/hub',
desired_capabilities=DesiredCapabilities.CHROME
)

driver.get('https://www.baidu.com')
print("get baidu")

driver.find_element_by_id("kw").send_keys("docker selenium")
driver.find_element_by_id("su").click()

sleep(1)

driver.get_screenshot_as_file("/home/fnngj/mypro/baidu_img.png")

driver.quit()
print("end...")