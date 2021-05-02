# -*- coding: utf-8 -*-
from projects.log_record.api.common_request.common import Common


class PageList(Common):
    u"""
    分页列表接口请求验证公共类
    """

    def __init__(self, content):
        super(PageList, self).__init__(content)
        request_data = content.post_data
        self._page_list_schema = {
            'useListCache': {'type': 'number', 'remark': '是否使用列表缓存'},
            'rowIndex': {'type': 'number', 'remark': '页码(由0开始)'},
            'listRows': {'type': 'number', 'remark': '页数'},
            'isGetPage': {'type': 'number', 'remark': '是否分页'},
        }
        self._page_list_error_message = {
            'useListCache': {'type': '列表获取类型必须'},
            'rowIndex': {'type': '页码类型必须为整形'},
            'listRows': {'type': '页数类型必须为整形'},
            'isGetPage': {'type': '分页类型必须为整形'},
        }
        self._row_index = request_data.get("rowIndex", 0)
        self._list_rows = request_data.get("listRows", 10)
        self._use_list_cache = request_data.get("useListCache", 1)
        self._is_get_page = request_data.get("isGetPage", 1)

    @property
    def is_get_page(self):
        return self._is_get_page

    @is_get_page.setter
    def is_get_page(self, value):
        self._is_get_page = value

    @property
    def use_list_cache(self):
        return self._use_list_cache

    @use_list_cache.setter
    def use_list_cache(self, value):
        self._use_list_cache = value

    @property
    def row_index(self):
        return self._row_index

    @row_index.setter
    def row_index(self, value):
        self._row_index = value

    @property
    def list_rows(self):
        return self._list_rows

    @list_rows.setter
    def list_rows(self, value):
        self._list_rows = value
