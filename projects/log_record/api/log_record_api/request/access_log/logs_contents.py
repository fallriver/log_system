#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : logs_contents.py
#    @Author   : sf_xu
#    @Time     : 2019/12/11 16:54
#
#    @Description  :

from handlers.content import Content
from projects.log_record.api.common_request.common import Common
from tools.validate import decorate_validate


class LogContentRequest(Common):
    """
    用户数据统计接口参数验证类
    """
    def __init__(self, content: Content):
        super(LogContentRequest, self).__init__(content)
        self._schema = {
            'firstDir': {'required': True, 'type': 'string', 'remark': "第一级目录"},
            'secondDir': {'required': True, 'type': 'string', 'remark': "第二级目录"},
            'fileName': {'required': True, 'type': 'string', 'remark': "日志文件名"},
            'num': {'type': 'string', 'remark': "条数"},
            'keywords': {'type': 'string', 'remark': "关键词"},
        }
        self._error_message = {
            'firstDir': {'required': "第一级目录必须", 'type': '第一级目录必须是字符串'},
            'secondDir': {'required': "第二级目录必须", 'type': '第二级目录必须是字符串'},
            'fileName': {'required': "日志文件名必须", 'type': '日志文件名必须是字符串'},
            'num': {'type': '条数必须是字符串'},
            'keywords': {'type': '关键词必须是字符串'},
        }
        post_data = content.post_data
        self._first_dir = post_data.get("firstDir", "")
        self._second_dir = post_data.get("secondDir", "")
        self._file_name = post_data.get("fileName", "")
        self._num = int(post_data.get("num", 100))
        self._keywords = post_data.get("keywords", "")

    @property
    def first_dir(self):
        return self._first_dir

    @property
    def second_dir(self):
        return self._second_dir

    @property
    def num(self):
        return self._num

    @property
    def file_name(self):
        return self._file_name

    @property
    def keywords(self):
        return self._keywords

    @decorate_validate
    def handle(self):
        u"""
        检查接口请求数据

        :return: self
        """
        return self