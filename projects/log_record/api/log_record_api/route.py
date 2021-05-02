# -*- coding: utf-8 -*-
import os

from exception.exception import SysException, BLException
from handlers.content import Content
from projects.log_record.api.log_record_api import api_class, api_name_list


can_ignore_api_list = []


class Route:

    def __init__(self, content: Content):
        self._api_name = ""  # 接口名称
        self._content = content  # 请求对象
        self._request_data = None  # 请求数据
        self._module = ""  # 接口模块

    def set_api_name(self):
        u"""
        设置接口名称

        :return: self
        """
        api_name = self._content.query_data.get("apiName", "")
        if not api_name:
            raise SysException(u"接口名必须")
        api_name.strip()
        self._api_name = api_name
        return self

    def set_request_data(self):
        u"""
        设置请求数据

        :return: self
        """
        request_data = self._content.post_data
        if not isinstance(request_data, dict):
            SysException(u"请求数据数据类型必须为字典")
        self._request_data = self._filter_request_data(request_data)
        return self

    def _filter_request_data(self, request_data):
        u"""
        过滤请求数据

        :param request_data dict 请求数据
        :return: request_data
        """
        for k, v in request_data.items():
            if isinstance(v, str):
                request_data[k] = v.strip()
        return request_data

    def set_api_module(self):
        for root, dirs, files in os.walk("projects/log_record/api/log_record_api/api_name_list"):
            for file in files:
                if os.path.splitext(file)[1] == '.py' and os.path.splitext(file)[0] != '__init__':
                    module = os.path.splitext(file)[0]
                    desModule = getattr(api_name_list, module)
                    name_list = desModule.api_name_list
                    for api_info in name_list:
                        if api_info['name'] == self._api_name:
                            self._module = module
                            break
        return True

    def route(self):
        self.set_api_name()
        self.set_request_data()
        self.set_api_module()

        if not self._module:
            raise BLException(u"接口不存在")
        desModule = getattr(api_class, self._module)
        desModule = getattr(desModule, self._api_name + "Api")
        if not desModule:
            SysException(u"找不到模块")
        ret = desModule(self._content).handle()
        return ret

    def __del__(self):
        pass