#!/usr/bin/env python
# coding=utf-8
import time
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor
from conf import base
from handlers.base import BaseHandler
from handlers.content import Content


class IndexHandler(BaseHandler):

    def get(self):
        res = self.back_handle()
        self.set_header("Content-Type", "application/json")
        self.finish(res)

    def post(self, *args, **kwargs):
        res = self.back_handle()
        self.set_header("Content-Type", "application/json")
        self.finish(res)

    def back_handle(self):
        content = self._get_req_obj()
        return content

    def _get_req_obj(self):
        return Content(handle=self)
