# -*- coding: utf-8 -*-
from exception.exception import SysException,BLException
from tools.cerberus import Validator
import functools

def decorate_validate(fn):
    u"""
    检查接口请求数据

    :param request_data dict 请求数据
    :return: Boolean
    """
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        request_data = getattr(self, "_request_data", None)
        if not isinstance(request_data, dict):
            raise SysException(u"请求数据数据类型必须为字典")
        schema = getattr(self, "_schema", None)
        error_message = getattr(self, "_error_message", None)
        if schema:
            v = Validator()
            v.validate(request_data, schema, error_message=error_message)
            if v.errors:
                for key in v.errors:
                    if not v.errors[key] or not isinstance(v.errors[key], list):
                        raise SysException(u"验证类发生错误")
                    if v.errors[key][0] != "unknown field":
                        raise BLException(v.errors[key][0])
        ret = fn(self, *args, **kwargs)
        return ret
    return wrapper