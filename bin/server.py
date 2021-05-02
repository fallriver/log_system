#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


__FILEPATH__ = os.path.abspath(__file__)
# 主要用来替换系统已经安装的库, 优先查找该目录
sys.path.insert(0, os.path.abspath(
    os.path.join(__FILEPATH__, os.pardir, os.pardir)))


from bin.app import Application
from handlers.index import IndexHandler
import os.path
import signal
import socket
import time
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.options
import tornado.web
from tornado.options import define, options
from conf import base
import importlib
from conf.base import VISIT_CONTENT

define("port", default=base.SERVER_PORT,
       help="run on the given port", type=int)

define("tornadoType", default=1, help="", type=int)
tornado.options.parse_command_line()

if options.tornadoType == 1:
    xsrf_cookies = False
else:
    xsrf_cookies = True

deadline = None


def sig_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    if VISIT_CONTENT:  # 关闭服务之前，写入日志
        from projects.log_record.ioc.import_log import VisitLogIoc
        VisitLogIoc(VISIT_CONTENT).save()
        VISIT_CONTENT.clear()  # 清空列表
    global deadline
    Application().log.debug(u"shutdown HTTPServer")
    http_server.stop()  # Stops listening for new connection
    io_loop = tornado.ioloop.IOLoop.instance()
    if deadline is None:
        deadline = time.time() + (base.REP_TIMEOUT / 1000)
    if base.ENV == 'DEBUG':
        Application().log.debug(u"debug model_fitting_hed, use cold shutdown")
        deadline = time.time()
    else:
        Application().log.debug(u"hot shutdowning, please wait %s s" % str(deadline - time.time()))

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            # 关闭I/O loop
            io_loop.stop()

    stop_loop()


# 加载动态路由器
route_list = [(r"/index", IndexHandler)]
par = os.path.abspath(
    os.path.join(__FILEPATH__, os.pardir, os.pardir, "projects/handlers"))
for project in os.listdir(par):
    if os.path.isdir(par + '/' + project) and project not in base.ignore_list:
        api_par = os.path.abspath(
            os.path.join(__FILEPATH__, os.pardir, os.pardir, "projects/handlers" + '/' + project))
        for api in os.listdir(api_par):
            if os.path.isfile(api_par + '/' + api) and api not in base.ignore_list:
                handlers = importlib.import_module('projects.handlers')
                pro_module = getattr(handlers, project)
                api = api.replace(".py", "")
                handler = getattr(pro_module, api)
                tmp = (r"/" + api, getattr(handler, "IndexHandler"))
                route_list.append(tmp)

bases = dict(
    xsrf_cookies=xsrf_cookies,
    debug=base.ENV == "DEBUG" and True or False,
    cookie_secret="cookie_secret_code",
    # login_url="/login",
    autoescape=None,
    # reserved=["user", "topic", "home", "base", "forgot", "login", "logout", "register", "admin"],
    handlers=route_list,
    autoreload=True
)
sockets = tornado.netutil.bind_sockets(options.port, address=base.BIND_IP, family=socket.AF_INET)
http_server = tornado.httpserver.HTTPServer(Application(**bases))
http_server.add_sockets(sockets)

signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGINT, sig_handler)

Application().log.debug("starting IOLoop ...")
tornado.ioloop.IOLoop.instance().start()
