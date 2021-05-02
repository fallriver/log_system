# -*- coding: utf-8 -*-

import tornado.web
from bin.log import logger


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

    def route(self, handlers):
        self.add_handlers('.*$', [(handlers.URL, handlers)])  # 路有关系映射添加到路由表中

    @property
    def log(self):
        return logger
