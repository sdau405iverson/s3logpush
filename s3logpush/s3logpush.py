#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue
from apscheduler.scheduler import Scheduler
import config
from custormer import Custormer
from logCollector import LogCollector
from run_logger import logger

#将扫描到的新增文件添加至队列
def producer(log_collectors):
    for log_collector in log_collectors:
        log_collector.collectLog()


def run():
    logger.info('服务启动，开始上传日志文件至S3')
    push_queue = Queue()
    log_collectors = []

    for i in range(config.PARALLEL_NUM):
        customer = Custormer(push_queue=push_queue, **config.S3_CONNECT)
        customer.start()

    #获取日志目录下的所有日志文件
    for app_log_info in config.APP_LOG_INFOS:
        log_collector = LogCollector(push_queue=push_queue, **app_log_info)
        log_collector.setup()
        log_collectors.append(log_collector)



    push_queue.join()
    #定时扫描日志目录的新增日志
    #sched = Scheduler(daemonic=False)
    #sched.start()
    #sched.add_cron_job(producer, args=(log_collectors,), **config.SCHEDULER)
    #sched.add_cron_job(producer, args=([1, 2, 3, 4, 5],), hour='0-23',minute='')
