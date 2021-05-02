#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : visit_log.py
#    @Author   : sf_xu
#    @Time     : 2019/12/10 15:02
#
#    @Description  :

api_name_list = [
    {"name": "ImportVisitLog",
     "desc": "记录访问日志",
     "api_type": "flow",  # 表示业务类型
     "is_auto_create": False, #表示是否自动生成文件
     },
    {"name": "GetLogsFolder",
     "desc": "获取日志文件夹",
     "api_type": "flow",  # 表示业务类型
     "is_auto_create": False,  # 表示是否自动生成文件
     },
    {"name": "GetLogsFile",
     "desc": "获取日志文件",
     "api_type": "flow",  # 表示业务类型
     "is_auto_create": False,  # 表示是否自动生成文件
     },
    {"name": "GetLogsContent",
     "desc": "获取日志文件内容",
     "api_type": "flow",  # 表示业务类型
     "is_auto_create": False,  # 表示是否自动生成文件
     },
]