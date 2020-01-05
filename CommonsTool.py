#!/usr/bin/env python
# -*- coding: utf-8 -*
import glob
import shutil

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import os

from Logging import Logs

log = Logs()

def wait_loading(driver):
    loading = (By.XPATH, '//div[@class="md-popup-box md-fade" and @style="display: none;"]')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(loading))


def rmdir5():
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("Eddid-News") + len("Eddid-News")]
    xml_report_pathlib = glob.glob(rootPath + r'\report\\xml*')
    html_report_pathlib = glob.glob(rootPath + r'\\report\\html*')

    try:
        html_report_name = rootPath + r'\report\html' + os.path.basename(xml_report_pathlib[-1])[3:]

    except IndexError:
        log.error("rmdir5, 数组越界")

    except Exception as e:
        raise e

    # 判断文件目录是否超过n个
    # 生成后才调用该方法, 所以要+1
    if len(xml_report_pathlib) >= 10:
        # shutil模块, 文件高级库
        shutil.rmtree(xml_report_pathlib[0])
    
    if len(html_report_pathlib) >= 50:
        # 删除第一个
        shutil.rmtree(html_report_pathlib[0])

    # self.gm.set_value(xml_report_path=xml_report_pathlib[-1])
    # self.gm.set_value(html_report_path=html_report_name)

    return xml_report_pathlib[-1], html_report_name

