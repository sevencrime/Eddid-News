#!/usr/bin/env python
# -*- coding: utf-8 -*
import glob
import os
import shutil
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from Commons.Logging import Logs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
    if len(xml_report_pathlib) >= 2:
        # shutil模块, 文件高级库
        shutil.rmtree(xml_report_pathlib[0])
    
    if len(html_report_pathlib) >= 30:
        # 删除第一个
        shutil.rmtree(html_report_pathlib[0])

    # self.gm.set_value(xml_report_path=xml_report_pathlib[-1])
    # self.gm.set_value(html_report_path=html_report_name)

    return xml_report_pathlib[-1], html_report_name


def set_details(s):
    # 转码邮件头
    name, addr = parseaddr(s)
    try:
        return formataddr((Header(name, 'utf-8').encode(), addr))
    except UnicodeDecodeError:
        return formataddr((Header(name, 'gbk')).encode(), addr)

def send_email(time, errfunc):
    smtp_server = "smtp.sina.cn"
    username = "15089514626@sina.cn"
    password = "Abcd1234"
    sendaddr = "onedi@qq.com"

    message = """
    <html>
         <head>
            <title> 资讯测试 </title>
         </head>
         <body>
            <p> 执行时间 : {time}</p>
            <p>报错的函数为 : {errfunc}</p>
            <br>
            <p>报告地址  <a>192.168.50.158:7777</a></p>
         </body>
    </html>
    """.format(time=time, errfunc="".join(n.name + ", " for n in errfunc))


    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = set_details("Onedi<{from_name}>".format(from_name=username))  #发送者
    msg['To'] = set_details("onedi<{to_url}>".format(to_url=sendaddr))      #接收者
    msg['Subject'] = Header("eddid-资讯数据出问题了啊!!!", 'utf-8').encode()     #标题

    smtpServer = smtplib.SMTP(smtp_server, 25)
    # smtpServer.set_debuglevel(1)
    smtpServer.login(username, password)
    smtpServer.sendmail(username, sendaddr, msg.as_string())
    smtpServer.quit()
