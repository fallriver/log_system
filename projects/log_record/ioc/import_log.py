#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : import_log.py
#    @Author   : sf_xu
#    @Time     : 2019/12/11 10:00
#
#    @Description  :


import os
import time


class VisitLogIoc(object):
    def __init__(self, log_content_list=None):
        self._log_content_list = log_content_list

    def save(self):
        u"""
        :return
        """
        # project_name = self._request_obj.project_name
        # log_type = self._request_obj.log_type
        # title = self._request_obj.title
        # content = self._request_obj.content

        for item in self._log_content_list:
            log_path = os.getcwd() + '/Logs/' + f"/{item['project_name']}/" + f"/{item['log_type']}/"
            if not os.path.exists(log_path):  # 判断文件路径是否存在
                os.makedirs(log_path)
            date = time.strftime('%Y%m%d', time.localtime(time.time()))
            log_name = log_path + date + '.log'
            data = f"{item['date_time']} - [title]:{item['title']} - [content]:{item['content']}"
            with open(log_name, mode="a+", encoding="utf8") as f:
                f.writelines(data + "\n")
                f.flush()

        return True


