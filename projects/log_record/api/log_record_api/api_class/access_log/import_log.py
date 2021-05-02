#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : import_log.py
#    @Author   : sf_xu
#    @Time     : 2019/12/10 14:34
#
#    @Description  :

# import sys
import time

from conf.base import LOG_SIZE, VISIT_CONTENT
from handlers.content import Content
from projects.log_record.api.log_record_api.request.access_log.import_visit_log import VisitLogRequest
from projects.log_record.ioc.import_log import VisitLogIoc


class ImportVisitLogApi(object):
    """写入访问日志记录"""
    def __init__(self, content: Content):
        self._request_obj = VisitLogRequest(content).handle()

    def handle(self):
        """
        执行接口内容
        :return: data
        """
        project_name = self._request_obj.project_name
        log_type = self._request_obj.log_type
        title = self._request_obj.title
        content = self._request_obj.content
        data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        VISIT_CONTENT.append({"date_time": data_time, "project_name": project_name, "log_type": log_type,
                              "title": title, "content": content})
        if len(VISIT_CONTENT) > LOG_SIZE:    # 日志暂存内容大于配置
            VisitLogIoc(VISIT_CONTENT).save()
            VISIT_CONTENT.clear()   # 清空列表
        return_data = {"msg": "操作成功", "data": len(VISIT_CONTENT)}
        return return_data
