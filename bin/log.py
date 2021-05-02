#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging.handlers
from conf import base as default

logger = logging.getLogger("tornado")
if not logger.handlers:
    handler = logging.handlers.RotatingFileHandler(
        default.LOG_FILE, maxBytes=1024 * 1024 * 10, backupCount=10)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)




