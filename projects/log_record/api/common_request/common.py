# -*- coding: utf-8 -*-

class Common(object):
    u"""
    接口验证请求公共类

    :param request object 请求对象
    :param request_data dict 请求参数
    :param kwargs dict 其他参数(预留字段)
    :param _schema dict 接收参数列表
    :param _error_message dict 接收参数错误规则信息
    :param _return_type string 返回参数类型
    :param _return dict 返回参数列表
    """

    def __init__(self, content=None):
        self._schema = {}
        self._error_message = {}
        self._return_type = ""
        self._return = {}
        self._request_data = content.post_data
        self._remote_ip = content.remote_ip
        self._op_uid = content.post_data.get("opUId", 0)

    @property
    def request_data(self):
        return self._request_data

    @property
    def remote_ip(self):
        return self._remote_ip

    @remote_ip.setter
    def remote_ip(self, value):
        self._remote_ip = value

    @property
    def op_uid(self):
        return self._op_uid

    @op_uid.setter
    def op_uid(self, value):
        self._op_uid = value

    def get_schema(self):
        return self._schema

    def get_error_message(self):
        return self._error_message

    def get_return_type(self):
        return self._return_type

    def get_return_data(self):
        return self._return

    def get_request_data(self):
        return self._request_data