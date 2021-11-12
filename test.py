# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  SignUper
@文件 :  test.py
@时间 :  2021/11/07 08:57
@作者 :  will
@版本 :  1.0
@说明 :   

'''
# from Utils import generates_random_user
#
# user=generates_random_user(20)
# print(user)
import os
import random
import re
import os
import platform
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Config import Config
from Utils import generates_random_user, get_domain_name, save_links, wait_get_element, read_file
from VerifyImage import VerifyImage
#
# def get_domain_name(url):
#     """
# 获取到网站域名中的名字
#     :param url:  要获取的网站
#     :return: 网站的名字
#     """
#     res = re.finditer(r'https?://(\w+)\.(\w+)\.?(\w*)?', url)
#     for site in res:
#         domain_list = site.groups()
#         if domain_list:
#             if domain_list[2]:
#                 return domain_list[1]
#             else:
#                 return domain_list[0]
#
#
# #
# print(domain_name)

# print(os.path.basename("/Users/will/Code/SignUper/test.json")[:-5])


# print(re.search(r"\d+\.\d+GB", "352MB"))

read_file("/Users/will/Code/SignUper/links/reoen.json")



# driver.find_element(By.ID,'aaa')
# 设置元素等待实例，最多等10秒，每0.5秒查看条件是否成立
# element = WebDriverWait(driver, 10, 0.5).until(
#     # 条件：直到元素加载完成
#     EC.presence_of_element_located((By.ID, "hahaha"))
# )
# print('哈哈哈')