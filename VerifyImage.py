# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  SignUper
@文件 :  VerifyImage.py
@时间 :  2021/11/07 07:55
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import time
from io import BytesIO
import random
from selenium import webdriver
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Config import Config
from Utils import wait_get_element


class VerifyImage(object):

    def __init__(self, driver):
        self.driver = driver
        pass

    def verify(self):
        self.driver.refresh()

        # 点击出现图片验证码
        embed_captcha = self.driver.find_element(By.XPATH, '//*[@id="embed-captcha"]')
        embed_captcha.click()
        time.sleep(1)
        # 获取到两张图片
        img1 = self.get_verify_image(False, "cc01.png")
        img2 = self.get_verify_image(True, "cc02.png")

        # 得到缺口的位置
        gap_position = self.get_gap_position(img1, img2)
        print("缺口位置：", gap_position)

        if not gap_position or gap_position <= 50:
            return False
        gap_position -= 2
        handle = self.driver.find_element(By.CSS_SELECTOR, ".geetest_slider_button")
        self.simulateDragX(handle, gap_position)
        # self.drag_handle(handle, gap_position)

        time.sleep(1)
        # 判断是否验证成功
        stag = self.driver.find_element(By.CSS_SELECTOR, ".geetest_success_radar_tip_content")
        if stag.size['width'] > 0:
            print('验证成功！')
            return True
        else:
            err_ele = self.driver.find_element(By.CSS_SELECTOR, ".geetest_result_content")
            if err_ele:
                err_msg = err_ele.text
            else:
                err_msg = ""

            print('验证失败:' + err_msg)
            return False

        pass

    def get_verify_image(self, gap_show, file_name=None):
        driver = self.driver
        capture_image_xpath = '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div'
        # 判断是否以无头方式运行
        if Config.CHROME_RUN_NO_HEAD:
            # 无头模式下的截图
            # 用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            # 将浏览器的宽高设置成刚刚获取的宽高
            driver.set_window_size(width, height)
            page_down = 0

        else:
            # 正常模式下的截图
            # 向下移动300像素
            page_down = 300
            self.driver.execute_script("window.scrollTo(0,%d)" % page_down)

        img = self.driver.find_element(By.CSS_SELECTOR, '.geetest_canvas_img')
        time.sleep(1)
        location = img.location
        size = img.size
        # 图片的偏移量
        top, bottom, left, right = location['y'] - page_down, location['y'] + size['height'] - page_down, location[
            'x'], location['x'] + size['width']
        # 是否显示缺口
        if gap_show:
            display = "none"
        else:
            display = 'block'
        self.driver.execute_script(
            "document.getElementsByClassName('geetest_canvas_fullbg')[0].style.display='%s';" % display)
        time.sleep(1)
        screenshot = driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        # 如果传入文件名则保存图片，否则不保存
        if file_name:
            captcha.save(file_name)
        return captcha
        pass

    # 获取缺口的位置
    def get_gap_position(self, img1, img2, left=50):
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

    def __getRadomPauseScondes(self):
        """
        :return:随机的拖动暂停时间
        """
        return random.uniform(0.6, 0.9)

    def simulateDragX(self, source, targetOffsetX):
        """
        模仿人的拖拽动作：快速沿着X轴拖动（存在误差），再暂停，然后修正误差
        防止被检测为机器人，出现“图片被怪物吃掉了”等验证失败的情况
        :param source:要拖拽的html元素
        :param targetOffsetX: 拖拽目标x轴距离
        :return: None
        """
        action_chains = webdriver.ActionChains(self.driver)
        # 点击，准备拖拽
        action_chains.click_and_hold(source)
        # 拖动次数，二到三次
        # dragCount = random.randint(2, 3)
        dragCount = 3
        if dragCount == 2:
            # 总误差值
            sumOffsetx = random.randint(-15, 15)
            action_chains.move_by_offset(targetOffsetX + sumOffsetx, 0)
            # 暂停一会
            action_chains.pause(self.__getRadomPauseScondes())
            # 修正误差，防止被检测为机器人，出现图片被怪物吃掉了等验证失败的情况
            action_chains.move_by_offset(-sumOffsetx, 0)
        elif dragCount == 3:
            # 总误差值
            sumOffsetx = random.randint(-25, 25)
            action_chains.move_by_offset(targetOffsetX + sumOffsetx, 0)
            # 暂停一会
            action_chains.pause(self.__getRadomPauseScondes())

            # 已修正误差的和
            fixedOffsetX = 0
            # 第一次修正误差
            if sumOffsetx < 0:
                offsetx = random.randint(sumOffsetx, 0)
            else:
                offsetx = random.randint(0, sumOffsetx)

            fixedOffsetX = fixedOffsetX + offsetx
            action_chains.move_by_offset(-offsetx, 0)
            action_chains.pause(self.__getRadomPauseScondes())

            # 最后一次修正误差
            action_chains.move_by_offset(-sumOffsetx + fixedOffsetX, 0)
            action_chains.pause(self.__getRadomPauseScondes())

        else:
            raise Exception("莫不是系统出现了问题？!")

        # 参考action_chains.drag_and_drop_by_offset()
        action_chains.release()
        action_chains.perform()

    def drag_handle(self, handle, gap_position):
        action_chains = webdriver.ActionChains(self.driver)
        action_chains.drag_and_drop_by_offset(handle, gap_position, 0)
        pass

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            print("浏览器退出失败！！！")
            print(e)
            exit(1)
            pass
