#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-30 下午5:49
import logging
import sys

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("AppName")

# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s 	%(filename)-4s %(lineno)-3d %(levelname)-8s: %(message)s')

# 文件日志
file_handler = logging.FileHandler("s3logpush_run.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)