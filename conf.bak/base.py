#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 环境配置
import os

ENV = "DEBUG"  # 环境主要有DEBUG ONLINE
BIND_IP = "0.0.0.0"  # 绑定ip
SERVER_PORT = 21003  # 默认监听端口
REP_TIMEOUT = 10  # 时间参数，等待时间 毫秒
CODE_VERSION = os.popen('git log --format="%H" -n 1').read()  # 版本
# POOL_RECYCLE = 110
# MAX_WORKERS = 1  # 最大进程数量
ignore_list = ["__pycache__", "__init__.py"]
# 日志配置
LOG_FILE = os.path.join("var", 'tornado.log')


