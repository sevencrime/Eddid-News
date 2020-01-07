from apscheduler.schedulers.blocking import BlockingScheduler

from src.Commons.Logging import Logs
from src.test_News import run


if __name__ == '__main__':
    log = Logs()
    # run()
    print("������ʱ����--30����ִ��һ��")
    apscheduler = BlockingScheduler()
    apscheduler.add_job(func=run, trigger='cron', minute='*/30')  #30����ִ��һ��
    apscheduler._logger = log
    apscheduler.start()