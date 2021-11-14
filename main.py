# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  SignUper
@文件 :  main.py
@时间 :  2021/11/07 07:54
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import time

from SignUper import SignUper

if __name__ == '__main__':
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('********************开始时间：' + strftime + '*******************')
    sign_uper = SignUper()
    sign_uper.signup()
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('********************结束时间：' + strftime + '*******************')

    pass
