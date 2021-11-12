#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件        :Utils.py
@时间        :2021/10/31 02:33:54
@作者        :Will
@版本        :1.0
@说明        :
'''
# 获取验证码图片
import os
from io import BytesIO
import json
import re
import time
import random
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generates_random_user(length=10):
    """
生成随机用户
    :param length: 用户名的长度，默认10
    :return: 生成的用户名
    """
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.sample(s, length))


def get_domain_name(url):
    """
获取到网站域名中的名字
    :param url:  要获取的网站
    :return: 网站的名字
    """
    res = re.finditer(r'https?://(\w+)\.(\w+)\.?(\w*)?', url)
    for site in res:
        domain_list = site.groups()
        if domain_list:
            if domain_list[2]:
                return domain_list[1]
            else:
                return domain_list[0]


def save_links(html, path):
    subLinks = {}
    # shadowrocket客户端
    tags = re.finditer(r'https?://.*?/link/.*\?\w+=shadowrocket', html)
    for tag in tags:
        subLinks['shadowrocket'] = tag.group()
    # Clash客户端
    tags = re.finditer(r'https?://.*?/link/.*\?clash=\w+', html)
    for tag in tags:
        subLinks['clash'] = tag.group()
    # V2ray客户端
    tags = re.finditer(r'https?://.*?/link/.*\?sub=3+', html)
    for tag in tags:
        subLinks['v2ray'] = tag.group()

    # 保存订阅链接
    write_file(path, json.dumps(subLinks))


def __getRadomPauseScondes():
    """
    :return:随机的拖动暂停时间
    """
    return random.uniform(0.6, 0.9)


def simulateDragX(dirver, source, targetOffsetX):
    """
    模仿人的拖拽动作：快速沿着X轴拖动（存在误差），再暂停，然后修正误差
    防止被检测为机器人，出现“图片被怪物吃掉了”等验证失败的情况
    :param source:要拖拽的html元素
    :param targetOffsetX: 拖拽目标x轴距离
    :return: None
    """
    action_chains = webdriver.ActionChains(dirver)
    # 点击，准备拖拽
    action_chains.click_and_hold(source)
    # 拖动次数，二到三次
    # dragCount = random.randint(2, 3)
    dragCount = 3
    if dragCount == 2:
        # 总误差值
        sumOffsetx = random.randint(-20, 20)
        action_chains.move_by_offset(targetOffsetX + sumOffsetx, 0)
        # 暂停一会
        action_chains.pause(__getRadomPauseScondes())
        # 修正误差，防止被检测为机器人，出现图片被怪物吃掉了等验证失败的情况
        action_chains.move_by_offset(-sumOffsetx, 0)
    elif dragCount == 3:
        # 总误差值
        sumOffsetx = random.randint(-20, 20)
        action_chains.move_by_offset(targetOffsetX + sumOffsetx, 0)
        # 暂停一会
        action_chains.pause(__getRadomPauseScondes())

        # 已修正误差的和
        fixedOffsetX = 0
        # 第一次修正误差
        if sumOffsetx < 0:
            offsetx = random.randint(sumOffsetx, 0)
        else:
            offsetx = random.randint(0, sumOffsetx)

        fixedOffsetX = fixedOffsetX + offsetx
        action_chains.move_by_offset(-offsetx, 0)
        action_chains.pause(__getRadomPauseScondes())

        # 最后一次修正误差
        action_chains.move_by_offset(-sumOffsetx + fixedOffsetX, 0)
        action_chains.pause(__getRadomPauseScondes())

    else:
        raise Exception("莫不是系统出现了问题？!")

    # 参考action_chains.drag_and_drop_by_offset()
    action_chains.release()
    action_chains.perform()


def getCapImage(driver, xpath, offsetY, fileName=''):
    # 用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")

    height = driver.execute_script("return document.documentElement.scrollHeight")

    # 获取页面宽度及其宽度
    print(width, height)

    # 将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, height)

    img = driver.find_element_by_xpath(xpath)
    time.sleep(0.5)
    location = img.location

    size = img.size

    print(location)
    print(size)
    # 图片的偏移量

    top, bottom, left, right = location['y'] + offsetY, location['y'] + \
                               size['height'] + offsetY, location['x'], location['x'] + size['width']
    screenshot = driver.get_screenshot_as_png()
    driver.get_screenshot_as_file('ss.png')
    screenshot = Image.open(BytesIO(screenshot))
    captcha = screenshot.crop((left, top, right, bottom))
    if fileName:
        captcha.save(fileName)
    return captcha


def wait_get_element(driver, by_cate, name, wait_time=20):
    element = None
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((by_cate, name))
        )
        return element
    except Exception as e:
        print(e)
        return element


# 获取缺口的位置
def getGapPos(img1, img2, left=50):
    # 定义像素差值的大小
    gap = 20
    # 将图片转换为黑白图片
    img1 = img1.convert("L")
    img2 = img2.convert("L")
    # 获取到图片的宽和高
    size = img1.size

    width = size[0]
    height = size[1]
    # print('验证图片宽：  高：', width, height)
    # 遍历所有的像素
    for x in range(left, width):
        for y in range(height):
            # 得到每个像素的值
            pixel1 = img1.load()[x, y]
            pixel2 = img2.load()[x, y]
            # 判断像素之间的差别
            pixelGap = abs(pixel1 - pixel2)
            # 如果像素之间的差值大于设定值直接返回
            if pixelGap >= gap:
                return x


def write_file(path, content):
    """
写入文件
    :param file: 文件路径
    :param content: 文件内容
    :return:
    """
    file = None
    try:
        # print(path)
        # print(content)
        file = open(path, "w", encoding='utf-8')
        file.write(content)
        file.close()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if file:
            file.close()


def read_file(file):
    """
读取文件
    :param file: 文件所在路径
    :return: 文件的内容
    """
    try:
        file = open(file, "r", encoding='utf-8')
        content = file.read()
        file.close()
        return content
    except Exception as e:
        if file:
            file.close()
        print(e)
        return False


def traverse_dir_files(root_dir, ext=None):
    """
    列出文件夹中的文件, 深度遍历
    :param root_dir: 根目录
    :param ext: 后缀名
    :param is_sorted: 是否排序，耗时较长
    :return: [文件路径列表, 文件名称列表]
    """
    names_list = []
    paths_list = []
    for parent, _, fileNames in os.walk(root_dir):

        for name in fileNames:
            if name.startswith('.'):  # 去除隐藏文件
                continue
            if ext:  # 根据后缀名搜索
                if name.endswith(tuple(ext)):
                    names_list.append(name)
                    paths_list.append(os.path.join(parent, name))
            else:
                names_list.append(name)
                paths_list.append(os.path.join(parent, name))
    return paths_list
