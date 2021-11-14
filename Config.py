# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  SignUper
@文件 :  Config.py
@时间 :  2021/11/07 08:07
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import os


class Config(object):
    # 浏览器是否以无头模式运行

    CHROME_NO_HEAD = False
    # 获取到当前的文件夹
    BASE_DIR = os.path.dirname(os.path.realpath('__file__'))
    # 订阅文件目录
    SUB_PATH = BASE_DIR + '/sub'
    # 下载订阅的链接文件目录
    LINK_PATH = BASE_DIR + '/links'
    # 日志目录
    LOG_PATH = BASE_DIR + '/logs'

    # 浏览器最终是否以无头的方法运行
    CHROME_RUN_NO_HEAD = False
    # 浏览器驱动位置
    CHROME_DIRVER_PATH = "libs"
    # 是否是Linux系统
    SYSTEM_IS_LINUX = False
    # 机场网址
    # AIRPORT_SITE_LIST = ['https://www.reoen.top']
    AIRPORT_SITE_LIST = [
        'https://xniuniu.xyz',
        'https://www.wiougong.fun',
        'https://www.jafiyun.icu'
    ]
