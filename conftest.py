#!/usr/bin/env python
# -*- coding: utf-8 -*-
from email.utils import parseaddr, formataddr

import pytest
import smtplib
from email.mime.text import MIMEText
from email.header import Header

pop_server = "imap.sina.cn"  # pop服务器
smtp_server = "smtp.sina.cn"
username = "15089514626@sina.cn"
password = "Abcd1234"
sendaddr = "onedi@qq.com"

def set_details(s):
    # 转码邮件头
    name, addr = parseaddr(s)
    try:
        return formataddr((Header(name, 'utf-8').encode(), addr))
    except UnicodeDecodeError:
        return formataddr((Header(name, 'gbk')).encode(), addr)


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
        if rep.failed:
        	# 捕获失败后, 发送邮件提示
        	# import pdb; pdb.set_trace()
        	# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
	        msg = MIMEText("测试发送", 'html', 'utf-8')
	        msg['From'] = set_details("Onedi<{from_name}>".format(from_name=username))	#发送者
	        msg['To'] = set_details("onedi<{to_url}>".format(to_url=sendaddr))		#接收者
	        msg['Subject'] = Header("eddid-资讯数据出问题了啊!!!", 'utf-8').encode()		#标题

	        smtpServer = smtplib.SMTP(smtp_server, 25)
	        # smtpServer.set_debuglevel(1)
	        smtpServer.login(username, password)
	        smtpServer.sendmail(username, sendaddr, msg.as_string())
	        smtpServer.quit()


