# -*- coding: utf-8 -*-
import os
import re
import sys
import traceback
import uuid

import simplejson
import tornado.web

# 对于Libs不做记录
from bin import Application
from conf import base

ignore_dirs = [re.compile(os.path.join(os.getcwd(), i)) for i in ['libs']]


class BaseHandler(tornado.web.RequestHandler):
    _unique_id = ""
    _remote_ip = ""

    def __init__(self, *argc, **argkw):
        self._content = None
        super(BaseHandler, self).__init__(*argc, **argkw)

    @property
    def unique_id(self):
        if not hasattr(self, "_uniqueId"):
            self._unique_id = str(uuid.uuid1())
        return self._unique_id

    @property
    def remote_ip(self):
        return self._remote_ip

    def get_connect(self, conn_name):
        return self.application.get_connect(conn_name)

    def set_default_header(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def render(self, template_name, **template_vars):
        html = self.render_string(template_name, **template_vars)
        self.write(html)

        @property
        def uniqueId(self):
            if not hasattr(self, "_uniqueId"):
                self._uniqueId = str(uuid.uuid1())
            return self._uniqueId

    def get_tb_err_file(self, excInfo):
        tb = ''.join(traceback.format_exception(*excInfo)[1:])
        err_files = re.findall('File "(.+)", line (\d+)', tb)
        for err_file in err_files[::-1]:
            if len(err_file) > 0:
                # 匹配是否存在应该忽略目录
                is_ignore = False
                for ignore_dir in ignore_dirs:
                    if re.match(ignore_dir, err_file[0]):
                        is_ignore = True
                        break
                # 如果报错目录为应该忽略目录, 忽略
                if is_ignore:
                    continue
                return err_file[0], err_file[1]
            else:
                continue
        else:
            return '', 0

    def _set_interface_error_log(self):
        """

        设置接口错误信息
        :return:
        """
        exc_info = sys.exc_info()
        tb = ''.join(traceback.format_exception(*exc_info)[1:])
        self.err_file, self.err_line = self.get_tb_err_file(exc_info)
        if os.path.exists(self.err_file):
            self.err_code = str(os.stat(self.err_file).st_ino) + ":" + str(self.err_line)
        else:
            self.err_code = ":" + str(self.err_line)
        post_data = self._content.post_data
        query_data = self._content.query_data
        data_dict = {"post_data":post_data, "query_data": query_data}
        data = str(simplejson.dumps(data_dict))
        api_name = str(self._content.api_name)
        remote_ip = self._content.remote_ip
        # 打印出错上下文
        err_log_list = list()
        err_log_list.append("index request start: %s\n" % self.unique_id)
        err_log_list.append("remoteIP: %s\n" % str(remote_ip))
        err_log_list.append("apiName: %s\n" % api_name)
        err_log_list.append("request_data: %s\n" % data)
        err_log_list.append("framework head git log commit id: %s" % base.CODE_VERSION)
        err_log_list.append("errcode: %s\n" % self.err_code)
        err_log_list.append("traceback: " + tb)
        err_log_list.append("index request end: %s" % self.unique_id)
        err_log = ''.join(err_log_list)
        Application().log.debug(err_log)
        return True
