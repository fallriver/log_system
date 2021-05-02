#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 中国联保日志系统一般接口入口
import time
from concurrent.futures import ThreadPoolExecutor

import simplejson
from tornado.web import HTTPError

from bin import Application
from conf import base
from exception.exception import SysException, BLException
from handlers.base import BaseHandler
from handlers.content import Content
from projects.log_record.api.log_record_api.route import Route

START_TIME = time.time()


class IndexHandler(BaseHandler):

    def get(self):
        res = self.back_handle()
        self.set_default_header()
        self.finish(res)

    def post(self, *args, **kwargs):
        if not base.VISIT_CONTENT:
            global START_TIME
            START_TIME = time.time()
        res = self.back_handle()
        self.set_default_header()
        self.finish(res)

    def options(self, *args, **kwargs):
        res = self.back_handle()
        self.set_default_header()
        self.finish(res)

    def on_finish(self):
        global START_TIME
        if time.time() - START_TIME >= base.LOG_TIME * 60:  # 达到配置时间，写入日志
            if base.VISIT_CONTENT:
                from projects.log_record.ioc.import_log import VisitLogIoc
                VisitLogIoc(base.VISIT_CONTENT).save()
                base.VISIT_CONTENT.clear()  # 清空列表
            START_TIME = time.time()

    def back_handle(self):
        return_date = {
            "code": 0,
            "msg": "获取成功",
            "request_id": self.unique_id,
            "data": {}
        }
        try:
            self._content = Content().set_handle(self).analysis()
            res = Route(self._content).route()
            if isinstance(res, dict) and res.get("msg"):
                return_date['msg'] = res.get("msg")
                del res['msg']
            if isinstance(res, dict) and res.get("data"):
                return_date['data'] = res.get("data")
                del res['data']
            else:
                return_date['data'] = res
        except BLException as e:
            return_date['code'] = e.code
            return_date['msg'] = e.msg
            self._set_interface_error_log()
        except SysException as e:
            return_date['code'] = e.code
            return_date['msg'] = e.msg
            self._set_interface_error_log()
        except HTTPError as e:
            return_date['code'] = e.status_code
            return_date['msg'] = e.reason
            self._set_interface_error_log()
        except Exception as e:
            error_message = getattr(e, "message", "系统异常")
            return_date['code'] = 500
            return_date['msg'] = error_message
            self._set_interface_error_log()
        finally:
            Application()
        Application()
        return simplejson.dumps(return_date)

