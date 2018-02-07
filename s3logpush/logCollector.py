#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import socket
import datetime
from run_logger import logger

IP_ADDR = socket.gethostbyname(socket.gethostname())
parten = re.compile(r'(\d+(-|_)?)+\d+')


class LogCollector():

    def __init__(self, push_queue=None, server_name=None, ip_addr=None, server_port=None, log_directory=None, name=None,
                 bucket=None):
        self.server_name = server_name
        self.ip_addr = IP_ADDR if ip_addr == '' else ip_addr
        self.server_port = server_port
        self.log_directory = log_directory
        self.name = name
        self.bucket = bucket
        self.logs_list = []
        self.push_queue = push_queue

    def setup(self):
        if os.path.isdir(self.log_directory):
            self.logs_list = self.base_dir_walk()
        else:
            logger.error("请检查目录(%s),是否可以访问" % (self.log_directory))
            sys.exit(1)
        for log_path in self.logs_list:
            if log_path != None:
                log_meto_info = {'path': log_path,
                                 'key': self.key_generater(log_path),
                                 'bucket': self.bucket}
                self.push_queue.put(log_meto_info)

    def base_dir_walk(self):
        logs_list = []
        for root, dirs, files in os.walk(self.log_directory):
            for file in files:
                logs_list.append(os.path.join(root, file))
        return logs_list

    def collectLog(self):
        current_logs_list = self.base_dir_walk(self.log_directory)
        new_added_logs = set(current_logs_list) - set(self.logs_list)
        for log_path in new_added_logs:
            if log_path != None:
                log_meto_info = {'path': log_path,
                                 'key': self.key_generater(log_path),
                                 'bucket': self.bucket}
                self.push_queue.put(log_meto_info)
        self.logs_list = current_logs_list

    def filefilter(self, log):
        base_name = os.path.basename(log)
        max_match = 0
        for m in parten.finditer(base_name):
            len_match = m.end() - m.start()
            max_match = max_match if max_match > len_match else len_match
        return log if max_match > 4 else None

    def filefilter_old(self, log):
        try:
            datetime.datetime.strptime(log, self.name)
            return os.path.join(self.log_directory, log)
        except ValueError as e:
            logger.info('%s与配置文件中定义的文件名称格式（%s）不匹配' % (log, self.name))

    def key_generater(self, log_path):
        return os.path.basename(self.log_directory) + '/' + log_path.lstrip(self.log_directory)

    def key_generater_old(self, log_name):
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
