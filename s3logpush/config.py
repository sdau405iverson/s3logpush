#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
S3_CONNECT = {'aws_access_key_id': 'YWRtaW4=',
              'aws_secret_access_key': '161ebd7d45089b3446ee4e0d86dbcf92',
              'endpoint_url': 'http://loganalyze.hcp1.kpw.tky.cn'}

APP_LOG_INFOS = [
    {'log_directory': '/home/samsing/pythonProjects/supersets','bucket': 'testdata'},
]

PARALLEL_NUM = 3

SCHEDULER = {'hour': '0-23', 'minute': '*', 'second': '*/2'}
