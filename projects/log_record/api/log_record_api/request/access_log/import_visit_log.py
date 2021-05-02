#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : import_visit_log.py
#    @Author   : sf_xu
#    @Time     : 2019/12/10 14:41
#
#    @Description  :


from handlers.content import Content
from projects.log_record.api.common_request.common import Common
from tools.validate import decorate_validate


class VisitLogRequest(Common):
    """
    用户数据统计接口参数验证类
    """
    def __init__(self, content: Content):
        super(VisitLogRequest, self).__init__(content)
        self._schema = {
            'projectName': {'required': True, 'type': 'string', 'remark': "项目名称"},
            'logType': {'required': True, 'type': 'string', 'remark': "日志类型"},
            'title': {'required': True, 'type': 'string', 'remark': "日志标题"},
            'content': {'required': True, 'type': 'string', 'remark': "日志内容"},
        }
        self._error_message = {
            'projectName': {'required': "项目名称必须", 'type': '项目名称必须是字符串'},
            'logType': {'required': "日志类型必须", 'type': '日志类型必须是字符串'},
            'title': {'required': "日志标题必须", 'type': "日志标题必须是字符串"},
            'content': {'required': "日志内容必须", 'type': "日志内容必须是字符串"},
        }

        post_data = content.post_data
        self._project_name = post_data.get("projectName", "")
        self._log_type = post_data.get("logType", "")
        self._title = post_data.get("title", "")
        self._content = post_data.get("content", "")

    @property
    def project_name(self):
        return self._project_name

    @property
    def log_type(self):
        return self._log_type

    @property
    def content(self):
        return self._content

    @property
    def title(self):
        return self._title

    @decorate_validate
    def handle(self):
        u"""
        检查接口请求数据

        :return: self
        """
        return self