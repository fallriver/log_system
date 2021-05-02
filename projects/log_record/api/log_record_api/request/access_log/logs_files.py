#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : logs_folder.py
#    @Author   : sf_xu
#    @Time     : 2019/12/11 11:36
#
#    @Description  :

from handlers.content import Content
from projects.log_record.api.common_request.common import Common
from tools.validate import decorate_validate


class LogFilesRequest(Common):
    """
    用户数据统计接口参数验证类
    """
    def __init__(self, content: Content):
        super(LogFilesRequest, self).__init__(content)
        self._schema = {
            'firstDir': {'required': True, 'type': 'string', 'remark': "第一级目录"},
            'secondDir': {'required': True, 'type': 'string', 'remark': "第二级目录"},
        }
        self._error_message = {
            'firstDir': {'required': "第一级目录必须", 'type': '第一级目录必须是字符串'},
            'secondDir': {'required': "第二级目录必须", 'type': '第二级目录必须是字符串'},
        }

        post_data = content.post_data
        self._first_dir = post_data.get("firstDir", "")
        self._second_dir = post_data.get("secondDir", "")

    @property
    def first_dir(self):
        return self._first_dir

    @property
    def second_dir(self):
        return self._second_dir

    @decorate_validate
    def handle(self):
        u"""
        检查接口请求数据

        :return: self
        """
        return self