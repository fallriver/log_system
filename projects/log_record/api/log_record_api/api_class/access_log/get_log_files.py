#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : get_log_files.py
#    @Author   : sf_xu
#    @Time     : 2019/12/11 15:32
#
#    @Description  :

import os

from handlers.content import Content
from projects.log_record.api.log_record_api.request.access_log.logs_files import LogFilesRequest


class GetLogsFileApi(object):
    """获取日志文件夹"""
    def __init__(self, content: Content):
        self._request_obj = LogFilesRequest(content).handle()

    def handle(self):
        """
        执行接口内容
        :return:
        """
        log_path = os.getcwd() + '/Logs/'
        first_dir = self._request_obj.first_dir
        second_dir = self._request_obj.second_dir
        complete_log_path = log_path + f"/{first_dir}/" + f"/{second_dir}/"
        files_list = os.listdir(complete_log_path)
        return files_list