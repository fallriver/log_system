#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SysException(Exception):
    def __init__(self, msg="请求错误", code=500):
        self.code = code
        self.msg = msg
        self.message = msg


class BLException(Exception):
    def __init__(self, msg="请求错误", code=400):
        self.code = code
        self.msg = msg
        self.message = msg


class WrongModelTypeException(Exception):
    pass


class RequestException(Exception):
    pass


class ResponseException(Exception):
    pass
