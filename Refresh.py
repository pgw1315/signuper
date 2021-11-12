# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  SignUper
@文件 :  Refresh.py
@时间 :  2021/11/07 08:03
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import json
import os
import time

import requests

from Config import Config
from Utils import traverse_dir_files, read_file, write_file


class Refresh(object):

    def __init__(self):
        pass

    def refresh(self):
        link_path_list = traverse_dir_files(Config.LINK_PATH)
        if link_path_list:
            strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('********************' + strftime + '*******************')
            for link_file in link_path_list:
                self.load_link_file(link_file)
            print("********************************************************")

    def load_link_file(self, link_file):
        contnent = read_file(link_file)
        if contnent:
            json_links = json.loads(contnent)
            site_name = os.path.basename(link_file)[:-5]
            # 文件加载成功，开始更新订阅
            print(site_name + '链接文件加载成功，开始更新订阅文件....')
            # 下载订阅文件
            for name, link in json_links.items():
                # 构建订阅文件地址
                file_name = site_name + "_" + name
                file_path = Config.SUB_PATH + "/" + file_name
                # 下载订阅文件
                res = requests.get(link)
                if res.status_code == 200:
                    try:
                        # 写入文件
                        if write_file(file_path, res.text):
                            print(file_name + ":订阅更新成功!")
                    except Exception as e:
                        print(file_name + '订阅链接，下载失败！！！')
                        print(e)
                        pass
                else:
                    print(file_name + '订阅链接，请求失败！！！')


if __name__ == '__main__':
    rf = Refresh()
    rf.refresh()
