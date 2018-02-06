#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
S3_CONNECT = {'aws_access_key_id': 'YWRtaW4=',
              'aws_secret_access_key': '161ebd7d45089b3446ee4e0d86dbcf92',
              'endpoint_url': 'http://loganalyze.hcp1.kpw.tky.cn'}
#日志备份的根目录
BASE_DIR = '/jboss/otswslog'

#日志备份根目录下以IP地址命名的所有目录
IP_ADDRS = [
    '10.2.201.10',
    '10.2.201.11',
    '10.2.201.12',
    '10.2.201.13',
    '10.2.201.14',
    '10.2.201.15',
    '10.2.201.16',
    '10.2.201.17',
    '10.2.201.18',
    '10.2.201.19',
    '10.2.201.2',
    '10.2.201.20',
    '10.2.201.21',
    '10.2.201.22',
    '10.2.201.23',
    '10.2.201.24',
    '10.2.201.25',
    '10.2.201.26',
    '10.2.201.27',
    '10.2.201.28',
    '10.2.201.29',
    '10.2.201.3',
    '10.2.201.30',
    '10.2.201.31',
    '10.2.201.32',
    '10.2.201.33',
    '10.2.201.4',
    '10.2.201.5',
    '10.2.201.6',
    '10.2.201.7',
    '10.2.201.8',
    '10.2.201.9',
]

#备份日志根目录下所有的服务分组
SERVERS = [
    #name: 服务分组名称
    #ports:该分组下的所有端口
    #log_name_format: 服务分组对应所有日志格式
    {'name': 'login',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['server.log.%Y-%m-%d-%H',
                         'bindLogger.log.%Y-%m-%d-%H',
                         'loginrecord.log.%Y-%m-%d-%H',
                         'sp.log.%Y-%m-%d-%H'
                         ],
     'bucket': 'partition3'
     },
    {'name': 'pay',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['server.log.%Y-%m-%d-%H',
                         'ccos.log.%Y-%m-%d-%H',
                         'passenger_redis.log.%Y-%m-%d-%H',
                         'sp.log.%Y-%m-%d-%H',
                         'innercallback.log.%Y-%m-%d-%H',
                         'httpnotify.log.%Y-%m-%d-%H'
                         ],
     'bucket': 'partition3'
     },
    {'name': 'tran',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['server.log.%Y-%m-%d-%H',
                         'monitor.log.%Y-%m-%d-%H',
                         'sp.log.%Y-%m-%d-%H',
                         'ccos.log.%Y-%m-%d-%H',
                         'passenger_redis.log.%Y-%m-%d-%H',
                         ],
     'bucket': 'partition3'
     },
    {'name': 'trsquery',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['server.log.%Y-%m-%d-%H',
                         'ccos.log.%Y-%m-%d-%H',
                         ],
     'bucket': 'partition3'
     },
    {'name': 'query',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['server.log.%Y-%m-%d-%H',
                         'monitor.log.%Y-%m-%d-%H',
                         'sp.log.%Y-%m-%d-%H',
                         'ccos.log.%Y-%m-%d-%H',
                         'leftQueryPara.log.%Y-%m-%d-%H',
                         'passenger_redis.log.%Y-%m-%d-%H'
                         ],
     'bucket': 'partition3'
     },
    {'name': 'otsmonitor/login',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['otswsmonitor.log.%Y-%m-%d'],
     'bucket': 'partition3'
     },
    {'name': 'otsmonitor/pay',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['otswsmonitor.log.%Y-%m-%d'],
     'bucket': 'partition3'
     },
    {'name': 'otsmonitor/tran',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['otswsmonitor.log.%Y-%m-%d'],
     'bucket': 'partition3'
     },
    {'name': 'otsmonitor/trsquery',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['otswsmonitor.log.%Y-%m-%d'],
     'bucket': 'partition3'
     },
    {'name': 'otsmonitor/query',
     'ports': ['otsws1', 'otsws2', 'otsws3', 'otsws4'],
     'log_name_format': ['otswsmonitor.log.%Y-%m-%d'],
     'bucket': 'partition3'
     },
]

APP_LOG_INFOS = []

#上传线程的并行数
PARALLEL_NUM = 3
# 定时任务执行时间定义,如下定义表示每个正点之后的第五分钟执行
SCHEDULER = {'hour': '0-23', 'minute': '5'}

for ip in IP_ADDRS:
    for server in SERVERS:
        for port in server['ports']:
            for log_name_format in server['log_name_format']:
                log_directory = os.path.join(BASE_DIR, ip, server['name'], port)
                if os.path.exists(log_directory):
                    app_log_info = {'server_name': server['name'],
                                'ip_addr': ip,
                                'server_port': port,
                                'log_directory': os.path.join(BASE_DIR, ip, server['name'], port),
                                'name': log_name_format,
                                'bucket': server['bucket']
                                }
                    APP_LOG_INFOS.append(app_log_info)
