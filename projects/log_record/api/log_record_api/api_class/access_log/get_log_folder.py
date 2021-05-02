#!/usr/bin/python
# -*- coding:utf-8 -*-
#    @fileName : get_log_folder.py
#    @Author   : sf_xu
#    @Time     : 2019/12/11 11:35
#
#    @Description  :
import os

from handlers.content import Content


class GetLogsFolderApi(object):
    """获取日志文件夹"""
    def __init__(self, content: Content):
        self._content = content

    def handle(self):
        """
        执行接口内容
        :return:
        """
        file_dict = {
            "folder": "Logs",
            "lower": ""
        }
        log_path = os.getcwd() + '/Logs/'
        second_folder = os.listdir(log_path)
        second_folder_list = []    # 第二级文件列表
        for folder in second_folder:
            third_folder = os.listdir(log_path + f"/{folder}/")
            third_folder_list = [{"folder": item, "lower": ""} for item in third_folder]  # 第三级文件列表
            second_folder_list.append({"folder": folder, "lower": third_folder_list})
        file_dict["lower"] = second_folder_list

        return file_dict