#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import subprocess
import random
import allure
import pytest
from apscheduler.schedulers.blocking import BlockingScheduler

from Commons import CommonsTool
from Commons.GlobalMap import GlobalMap
from Commons.Logging import Logs
from News_API import get_flashAPI, bank_report_API, calendar_data_API, calendar_event_API, calendar_holiday_API
from pages.GET_New_flash import News_Flash
from pages.GET_News_bankReport import Bank_Report
from pages.GET_News_calendar import News_calendar

# 生产环境
url = 'https://download.eddidapp.com/page/eddid-news/index.html'
# uat环境
# url = 'https://download.eddidapp.com/page/eddid-news-dev/index.html'

log = Logs()
log.debug("开始执行程序 {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))



@allure.feature("校验快讯-期货的数据")
@allure.description("affect有值时 : pagelist['content'] == apilist['data']['country'] + apilist['data']['time_period'] + apilist['data']['name']\n\n"
                    "affect == 0 时, actual > (预测值 or 前值) 为 利多, 反则为利空\n\n"
                    "affect == 1 时, actual < (预测值 or 前值) 为 利多, 反则为利空"
                    )
def test_flash_futures(driver):
    # 快讯-期货
    n = News_Flash(driver, url)
    with allure.step("爬取快讯-期货页面数据"):
        flashList, addflashList, opentime = n.get_flash_futures()

    with allure.step("调用快讯-期货接口"):
        allure.attach('', '调用接口的时间:{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), allure.attachment_type.TEXT)
        flash_api_list = get_flashAPI(channel=-8200)

    with allure.step("对比数据"):
        n.same_flashData(flashList, flash_api_list['data'])

    with allure.step("再次调用快讯-期货接口, 模拟加载更多"):
        # 获取接口最后一条时间减少一秒
        strtime = datetime.datetime.strptime(flash_api_list['data'][-1]['time'], "%Y-%m-%d %H:%M:%S")
        startTime = (strtime - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
        newflash_api_list = get_flashAPI(channel=-8200, max_time = startTime)

    with allure.step("模拟加载更多后对比数据"):
        n.same_flashData(addflashList, flash_api_list['data'] + newflash_api_list['data'])

@allure.feature("校验快讯-港美股的数据")
@allure.description("有利空利多 : pagelist['content'] == apilist['data']['country'] + apilist['data']['time_period'] + apilist['data']['name']\n\n"
                    "affect == 0 时, actual > (预测值 or 前值) 为 利多, 反则为利空\n\n"
                    "affect == 1 时, actual < (预测值 or 前值) 为 利多, 反则为利空"
                    )
def test_flash_HK(driver):
    # 快讯 -港美股
    n = News_Flash(driver, url)
    with allure.step("爬取快讯-港美股页面数据"):
        flashList, addflashList, opentime = n.get_flash_HK()

    with allure.step("调用快讯-港美股接口"):
        allure.attach('', '调用接口的时间:{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), allure.attachment_type.TEXT)
        flash_api_list = get_flashAPI(channel=3)

    with allure.step("对比数据"):
        n.same_flashData(flashList, flash_api_list['data'])

    with allure.step("再次调用快讯-港美股接口, 模拟加载更多"):
        strtime = datetime.datetime.strptime(flash_api_list['data'][-1]['time'], "%Y-%m-%d %H:%M:%S")
        startTime = (strtime - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
        newflash_api_list = get_flashAPI(channel=3, max_time = startTime)

    with allure.step("模拟加载更多后对比数据"):
        n.same_flashData(addflashList, flash_api_list['data'] + newflash_api_list['data'])


@allure.feature("校验投行报告-港股目标价的数据")
def test_bankReport_hk(driver):
    # 实例化
    br = Bank_Report(driver, url)
    with allure.step("爬取投行报告-港股目标价页面数据"):
        # 开始获取投行报告页面的数据
        bankReportList, add_bankReportList = br.get_bank_report_hk()

    with allure.step("调用投行报告-港股目标价接口"):
        # 请求投行报告接口, 返回全部数据
        API_bankReportlist = bank_report_API(category=["hk"])

    with allure.step("对比数据"):
        # 对比数据
        br.same_listofdict(bankReportList, API_bankReportlist)
        br.same_listofdict(add_bankReportList, API_bankReportlist)

@allure.feature("校验投行报告-美股目标价的数据")
def test_bankReport_us(driver):
    # 实例化
    br = Bank_Report(driver, url)

    with allure.step("爬取投行报告-美股目标价页面数据"):
        # 开始获取投行报告页面的数据
        bankReportList, add_bankReportList = br.get_bank_report_us()

    with allure.step("调用投行报告-港股目标价接口"):
        # 请求投行报告接口, 返回全部数据
        API_bankReportlist = bank_report_API(category=["us"])

    with allure.step("对比数据"):
        # 对比数据
        br.same_listofdict(bankReportList, API_bankReportlist)
        br.same_listofdict(add_bankReportList, API_bankReportlist)

# 日历-数据-当天
@allure.feature("校验日历-数据--当天的数据")
@allure.description("pagelist[i]['title'] == (apilist[i]['country'] + apilist[i]['time_period'] + apilist[i]['indicator_name'])")
def test_calendar_date(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-数据页面数据"):
        nowtime = datetime.datetime.now().strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(nowtime))
        allure.attach('', '打开的日期:{}'.format(nowtime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartime=nowtime)

    with allure.step("调用日历-数据接口"):
        # 调用接口
        dataAPI_list = calendar_data_API(nowtime)

    with allure.step("对比数据"):
        calendar.same_data(calendardataList, dataAPI_list)

# 日历-数据-以前日期
@allure.feature("校验日历-数据--以前日期的数据")
@allure.description("pagelist[i]['title'] == (apilist[i]['country'] + apilist[i]['time_period'] + apilist[i]['indicator_name'])")
def test_calendar_before(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-数据页面数据"):
        nowtime = datetime.datetime.now()
        # startTime = (nowtime - datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        # 暂时写死, 不能滑动
        startTime = (nowtime - datetime.timedelta(days=2)).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartime=startTime)

    with allure.step("调用日历-数据接口"):
        # 调用接口
        dataAPI_list = calendar_data_API(startTime)

    with allure.step("对比数据"):
        calendar.same_data(calendardataList, dataAPI_list)

# 日历-数据-未来日期
@allure.feature("校验日历-数据--未来日期的数据")
@allure.description("pagelist[i]['title'] == (apilist[i]['country'] + apilist[i]['time_period'] + apilist[i]['indicator_name'])")
def test_calendar_after(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-数据页面数据"):
        nowtime = datetime.datetime.now()
        startTime = (nowtime + datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartime=startTime)

    with allure.step("调用日历-数据接口"):
        # 调用接口
        dataAPI_list = calendar_data_API(startTime)

    with allure.step("对比数据"):
        calendar.same_data(calendardataList, dataAPI_list)


# 日历-财经事件-当天
@allure.feature("校验日历-财经事件--当天的数据")
def test_calendar_event_date(driver):
    calendar = News_calendar(driver, url)
    with allure.step("爬取日历-财经事件页面数据"):
        nowtime = datetime.datetime.now().strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(nowtime))
        allure.attach('', '打开的日期:{}'.format(nowtime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartime=nowtime, calendartab="财经事件")

    with allure.step("调用日历-财经事件接口"):
        # 调用接口
        dataAPI_list = calendar_event_API(nowtime)

    with allure.step("对比数据"):
        calendar.same_event(calendardataList, dataAPI_list)

# 日历-财经事件-以前日期
@allure.feature("校验日历-财经事件--以前日期的数据")
def test_calendar_event_before(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-财经事件页面数据"):
        nowtime = datetime.datetime.now()
        # startTime = (nowtime - datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        # 暂时写死, 不能滑动
        startTime = (nowtime - datetime.timedelta(days=2)).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="财经事件", calendartime=startTime)

    with allure.step("请求日历--财经事件接口"):
        # 调用接口
        dataAPI_list = calendar_event_API(startTime)

    with allure.step("对比数据"):
        calendar.same_event(calendardataList, dataAPI_list)

# 日历-财经事件-未来日期
@allure.feature("校验日历-财经事件--未来日期的数据")
def test_calendar_event_after(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-财经事件页面数据"):
        nowtime = datetime.datetime.now()
        startTime = (nowtime + datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="财经事件", calendartime=startTime)

    with allure.step("请求日历--财经事件接口"):
        # 调用接口
        dataAPI_list = calendar_event_API(startTime)

    with allure.step("对比数据"):
        calendar.same_event(calendardataList, dataAPI_list)

# 日历-美港财报-当天
@allure.feature("校验日历-美港财报--当天的数据")
@allure.description("pagelist[i]['title'] == (apilist[i]['indicator_name'] + apilist[i]['time_period'])")
def test_calendar_stock_date(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-美港财报页面数据"):
        nowtime = datetime.datetime.now().strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(nowtime))
        allure.attach('', '打开的日期:{}'.format(nowtime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="美港财报")

    with allure.step("请求日历-美港财报接口"):
        dataAPI_list = calendar_data_API(nowtime, stock=True)

    with allure.step("对比数据"):
        calendar.same_data(calendardataList, dataAPI_list, stock=True)

# 日历-美港财报-以前日期
@allure.feature("校验日历-美港财报--以前日期的数据")
@allure.description("pagelist[i]['title'] == (apilist[i]['indicator_name'] + apilist[i]['time_period'])")
def test_calendar_stock_before(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-美港财报页面数据"):
        nowtime = datetime.datetime.now()
        # startTime = (nowtime - datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        # 暂时写死, 不能滑动
        startTime = (nowtime - datetime.timedelta(days=2)).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="美港财报", calendartime=startTime)

    with allure.step("请求日历-美港财报接口"):
        # 调用接口
        dataAPI_list = calendar_data_API(startTime, stock=True)

    with allure.step("对比数据"):
        calendar.same_data(calendardataList, dataAPI_list, stock=True)

# 日历-美港财报-未来日期
@allure.feature("校验日历-美港财报--未来日期的数据")
@allure.description("pagelist[i]['title'] == (apilist[i]['indicator_name'] + apilist[i]['time_period'])")
def test_calendar_stock_after(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-美港财报页面数据"):
        nowtime = datetime.datetime.now()
        startTime = (nowtime + datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="美港财报", calendartime=startTime)

    with allure.step("请求日历-美港财报接口"):
        # 调用接口
        dataAPI_list = calendar_data_API(startTime, stock=True)

    with allure.step("对比数据"):
        calendar.same_data(calendardataList, dataAPI_list, stock=True)

# 日历-假期-当天
@allure.feature("校验日历-假期--当天的数据")
@allure.description("pagelist[i]['name'] == apilist[i]['country'] + '/' + apilist[i]['name']\n\n"
                    "pagelist[i]['title'] == apilist[i]['exchange_name'] + apilist[i]['rest_note']")
def test_calendar_holiday_date(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-假期页面数据"):
        nowtime = datetime.datetime.now().strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(nowtime))
        allure.attach('', '打开的日期:{}'.format(nowtime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="假期")

    with allure.step("请求日历-假期接口"):
        # 调用接口
        dataAPI_list = calendar_holiday_API(nowtime)

    with allure.step("对比数据"):
        calendar.same_holiday(calendardataList, dataAPI_list)

# 日历-假期-以前日期
@allure.feature("校验日历-假期--以前日期的数据")
@allure.description("pagelist[i]['name'] == apilist[i]['country'] + '/' + apilist[i]['name']\n\n"
                    "pagelist[i]['title'] == apilist[i]['exchange_name'] + apilist[i]['rest_note']")
def test_calendar_holiday_before(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-假期页面数据"):
        nowtime = datetime.datetime.now()
        # startTime = (nowtime - datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        # 暂时写死, 不能滑动
        startTime = (nowtime - datetime.timedelta(days=2)).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="假期", calendartime=startTime)

    with allure.step("请求日历-假期接口"):
        # 调用接口
        dataAPI_list = calendar_holiday_API(startTime)

    with allure.step("对比数据"):
        calendar.same_holiday(calendardataList, dataAPI_list)

# 日历-假期-未来日期
@allure.feature("校验日历-假期--未来日期的数据")
@allure.description("pagelist[i]['name'] == apilist[i]['country'] + '/' + apilist[i]['name']\n\n"
                    "pagelist[i]['title'] == apilist[i]['exchange_name'] + apilist[i]['rest_note']")
def test_calendar_holiday_after(driver):
    calendar = News_calendar(driver, url)

    with allure.step("爬取日历-假期页面数据"):
        nowtime = datetime.datetime.now()
        startTime = (nowtime + datetime.timedelta(days=random.randint(1, 15))).strftime("%Y%m%d")
        log.info("打开的日期为 {}".format(startTime))
        allure.attach('', '打开的日期:{}'.format(startTime), allure.attachment_type.TEXT)
        # 爬页面
        calendardataList = calendar.get_calendar_data(calendartab="假期", calendartime=startTime)

    with allure.step("请求日历-假期接口"):
        # 调用接口
        dataAPI_list = calendar_holiday_API(startTime)

    with allure.step("对比数据"):
        calendar.same_holiday(calendardataList, dataAPI_list)

def run():
    print("开始执行程序 {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')))
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("Eddid-News") + len("Eddid-News")]
    gm = GlobalMap()
    gm.set_List("errfunc", [])
    gm.set_value(nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

    pytest.main(["-s", "-v", "test_News.py",
                 "--alluredir",
                 rootPath + '/report/xml_{time}'.format(time=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')),
                 "--reruns=2",  # pip install pytest-rerunfailures
                 "--reruns-delay=2"
                 ])
    xml_report_path, html_report_path = CommonsTool.rmdir5()
    print(xml_report_path)
    print(html_report_path)
    os.popen("allure generate {xml_report_path} -o {html_report_path} --clean".format(xml_report_path=xml_report_path, html_report_path=html_report_path)).read()

    if gm.get_value("errfunc") != [] and gm.get_value("errfunc") != 'Null_':
        # 发送邮件提醒
        CommonsTool.send_email(gm.get_value("nowtime"), gm.get_value("errfunc"))
        # 删除变量
        gm.del_map("errfunc")
        gm.del_map("errmsg")



if __name__ =='__main__':
    # run()
    print("启动定时任务", datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    apscheduler = BlockingScheduler()
    apscheduler.add_job(func=run, trigger='cron', minute='*/10')  #30分钟执行一次
    apscheduler._logger = log
    apscheduler.start()