#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from src.Commons.Logging import Logs
from src.test_News import run

if __name__ == '__main__':
    log = Logs()
    run()
    # print("启动定时任务--30分钟执行一次")
    # apscheduler = BlockingScheduler()
    # apscheduler.add_job(func=run, trigger='cron', minute='*/10')  #30分钟执行一次
    # apscheduler._logger = log
    # apscheduler.start()