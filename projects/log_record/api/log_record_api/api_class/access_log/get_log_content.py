#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : get_log_content.py
#    @Author   : sf_xu
#    @Time     : 2019/12/11 16:27
#
#    @Description  :

import os

from handlers.content import Content
from projects.log_record.api.log_record_api.request.access_log.logs_contents import LogContentRequest


class GetLogsContentApi(object):
    """获取日志内容"""
    def __init__(self, content: Content):
        self._request_obj = LogContentRequest(content).handle()

    def handle(self):
        """
        执行接口内容
        :return:
        """
        log_path = os.getcwd() + '/Logs/'
        first_dir = self._request_obj.first_dir
        second_dir = self._request_obj.second_dir
        file_name = self._request_obj.file_name
        keywords = str(self._request_obj.keywords).lstrip()
        
        num = self._request_obj.num
        complete_log_file_path = log_path + f"{first_dir}/" + f"{second_dir}/" + f"{file_name}"
        if not keywords:  # 条数搜索
            content = os.popen(f" head -{num} {complete_log_file_path}").read()
        else:  # 关键字搜索
            content = os.popen(f" grep -r '{keywords}' {complete_log_file_path}").read()
        if not content:
            return_data = []
        else:
            return_data = content.split("\n")[:-1]
        return return_data


