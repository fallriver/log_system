#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson

from exception.exception import SysException
from tools.wx.util.parser import XMLStore


class Content:
    def __init__(self):
        """
        :param handle:请求基类
        """
        self._handle = None
        # 头数据
        self._header_data = {}
        # get数据
        self._query_data = {}
        # post数据
        self._post_data = {}
        # remote_ip
        self._remote_ip = ""
        # api_name
        self._api_name = ""

    @property
    def api_name(self):
        if not self._api_name:
            self._api_name = self.query_data.get("apiName")
        return self._api_name

    @api_name.setter
    def api_name(self, value):
        self._api_name = value

    def set_handle(self, value):
        self._handle = value
        return self

    @property
    def remote_ip(self):
        return self._remote_ip

    @property
    def header_data(self):
        return self._header_data

    @header_data.setter
    def header_data(self, value):
        self._header_data = value

    @property
    def query_data(self):
        return self._query_data

    @query_data.setter
    def query_data(self, value):
        self._query_data = value

    @property
    def post_data(self):
        return self._post_data

    @post_data.setter
    def post_data(self, value):
        self._post_data = value

    def _analysis_header_data(self):
        """
        header参数解析
        :return: 
        """
        self._header_data = self._handle.request.headers

    def _analysis_query_data(self):
        """
        get请求参数解析
        """

        query_arguments = self._handle.request.query_arguments
        self._query_data = {x: query_arguments.get(x)[0].decode("utf-8") for x in query_arguments.keys()}

    def _analysis_post_data(self):
        """
        post请求参数解析
        """
        request = self._handle.request
        content_type = self.header_data.get("Content-Type")
        if not content_type:
            self._post_data = {}
            return True
        if "application/json" in content_type:
            post_data = request.body
            if post_data:
                try:
                    self._post_data = simplejson.loads(post_data.decode('utf-8'))
                except:
                    raise SysException("post_data 不是json格式")
        elif "form-data" in content_type:
            post_data = request.body_arguments
            self._post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        elif "x-www-form-urlencoded" in content_type:
            post_data = request.body_arguments
            self._post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        elif "xml" in content_type:
            post_data = request.body.decode('utf-8')
            try:
                self._post_data = XMLStore(post_data).xml2dict
            except Exception:
                raise SysException("post_data 不是xml格式")
        else:
            raise SysException("未知post请求类似")
        return True

    def _analysis_remote_ip(self):
        self._remote_ip = self._post_data.get("remoteIP") if self._post_data.get("remoteIP") else self._handle.request.remote_ip

    def analysis(self):
        self._analysis_header_data()
        self._analysis_query_data()
        self._analysis_post_data()
        self._analysis_remote_ip()
        return self
