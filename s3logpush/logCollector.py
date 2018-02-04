#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import datetime
from run_logger import logger
from threading import Thread

import socket

IP_ADDR = socket.gethostbyname(socket.gethostname())


class LogCollector(Thread):

    def __init__(self, push_queue=None, server_name=None,ip_addr=None, server_port=None, log_directory=None, name=None, bucket=None):
        Thread.__init__(self,)
        self.daemon = False
        self.server_name = server_name
        self.ip_addr = IP_ADDR if ip_addr == '' else ip_addr
        self.server_port = server_port
        self.log_directory = log_directory.replace('$server_name', server_name).replace('$server_port', server_port)
        self.name = name
        self.bucket = bucket
        self.logs_list = None
        self.push_queue = push_queue

    def run(self):
        self.setup()

    def setup(self):
        try:
            self.logs_list = os.listdir(self.log_directory)
        except OSError as e:
            logger.error("请检查目录(%s),是否可以访问" % (self.log_directory))
            sys.exit(1)
        for log_name in self.logs_list:
            log_path = self.filefilter(log_name)
            if log_path != None:
                log_meto_info = {'path': log_path,
                                 'key': self.key_generater(log_name),
                                 'bucket': self.bucket}
                self.push_queue.put(log_meto_info)

    def collectLog(self):
        current_logs_list = os.listdir(self.log_directory)
        new_added_logs = set(current_logs_list) - set(self.logs_list)
        for new_added in new_added_logs:
            log_path = self.filefilter(new_added)
            if log_path != None:
                log_meto_info = {'path': log_path,
                                 'key': self.key_generater(new_added),
                                 'bucket': self.bucket}
                self.push_queue.put(log_meto_info)
        self.logs_list = current_logs_list

    def filefilter(self, log):
        try:
            datetime.datetime.strptime(log, self.name)
            return os.path.join(self.log_directory, log)
        except ValueError as e:
            logger.info('%s与配置文件中定义的文件名称格式（%s）不匹配' % (log, self.name))

    def key_generater(self, log_name):
        log_datetime = datetime.datetime.strptime(log_name, self.name)
        log_date = datetime.datetime.strftime(log_datetime, '%Y%m%d')
        new_log_name = self.get_lognewname(log_name)
        key = '/'.join([self.server_name, log_date, new_log_name])
        return key


    def get_lognewname(self, log_name):
        log_name_contents = list(os.path.splitext(log_name))
        if '.log' == log_name_contents[-1]:
            log_name_contents.insert(-1, '-'.join(('', self.ip_addr, self.server_port)))
        else:
            log_name_contents.append('-'.join(('', self.ip_addr, self.server_port)))
        new_log_name = ''.join(log_name_contents)
        return new_log_name
