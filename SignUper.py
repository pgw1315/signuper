# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  SignUper
@文件 :  SignUper.py
@时间 :  2021/11/07 07:58
@作者 :  will
@版本 :  1.0
@说明 :

'''
import os
import platform
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Config import Config
from Utils import generates_random_user, get_domain_name, save_links, wait_get_element
from VerifyImage import VerifyImage


class SignUper(object):
    def init_env(self):
        """
初始化运行环境
        """
        # 初始化目录
        if not os.path.isdir(Config.LINK_PATH):
            os.makedirs(Config.LINK_PATH)
        if not os.path.isdir(Config.SUB_PATH):
            os.makedirs(Config.SUB_PATH)
        if not os.path.isdir(Config.LOG_PATH):
            os.makedirs(Config.LOG_PATH)
        # 初始化驱动
        sysstr = platform.system()
        if sysstr == "Linux":
            # print("当前使用的是Linux系统")
            Config.CHROME_DIRVER_PATH += '/chromedriver'
            Config.SYSTEM_IS_LINUX = True
        else:
            # print("当前使用的是其他系统")
            Config.CHROME_DIRVER_PATH += '/mac_chromedriver'
            Config.SYSTEM_IS_LINUX = False
        pass

    def init_dirver(self):
        """
初始化驱动所有设置
        """
        chrome_options = Options()
        # 设置浏览器是否无头运行，如果是Linux系统则默认无头运行，如果是其他系统，则根据CHROME_NO_HEAD的值决定是否无头运行呢
        if Config.SYSTEM_IS_LINUX:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')  # 禁止沙箱模式，否则肯能会报错遇到chrome异常
            Config.CHROME_RUN_NO_HEAD = True
        else:
            if Config.CHROME_NO_HEAD:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')  # 禁止沙箱模式，否则肯能会报错遇到chrome异常
                Config.CHROME_RUN_NO_HEAD = True
        driver = webdriver.Chrome(executable_path=Config.CHROME_DIRVER_PATH, chrome_options=chrome_options)
        driver.maximize_window()
        # 隐式等待
        driver.implicitly_wait(20)
        return driver

    def __init__(self):
        self.user = generates_random_user()
        self.init_env()

        pass

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            print("浏览器退出失败！！！")
            print(e)
            exit(1)
            pass

    def signup(self):
        for site in Config.AIRPORT_SITE_LIST:
            site_reg_url = site + '/auth/register'
            try:
                self.driver = self.init_dirver()
                self.driver.get(site_reg_url)
                print('打开网址：' + site_reg_url)
            except Exception as e:
                print('打开网址出错了！！')
                print(e)
                self.close()
                pass
            verify_image = VerifyImage(self.driver)
            is_verify = False
            try:
                # 开始检查是否有验证码
                print('开始检查是否有验证码')
                time.sleep(1)
                self.driver.find_element(By.ID, "embed-captcha")
                is_verify = True
            except:
                is_verify = False
                pass
            # 判断是否有验证码
            if is_verify:
                print('开始验证图片...')
                success = False
                while not success:
                    success = verify_image.verify()
            # 自动填写表单
            self.fill_form()
            # 自动完成后续
            self.auto_complete(site)

        pass

    def auto_complete(self, site):

        try:
            time.sleep(3)
            # 点击注册完成按钮
            element = self.driver.find_element(By.CSS_SELECTOR, '.swal2-confirm')
            element.click()
            print('注册成功:' + self.user)
            time.sleep(3)
            # 点击签到
            self.driver.find_element(By.ID, 'checkin-div').click()
            print('签到完成！')
            # 匹配域名
            domain_name = get_domain_name(site)
            if not domain_name:
                domain_name = 'default'
            print(domain_name)

            html = self.driver.execute_script("return document.documentElement.outerHTML")
            # 保存链接文件
            links_json = Config.LINK_PATH + "/" + domain_name + ".json"
            save_links(html, links_json)
            print('订阅链接保存完成')
            time.sleep(3)
            self.close()
        except Exception as e:
            print('注册失败')
            print(e)
            self.close()
            pass

    def fill_form(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "#name").send_keys(self.user)
            self.driver.find_element(By.CSS_SELECTOR, "#email").send_keys(self.user)
            self.driver.find_element(By.CSS_SELECTOR, "#passwd").send_keys(self.user)
            self.driver.find_element(By.CSS_SELECTOR, "#repasswd").send_keys(self.user)
            self.driver.find_element(By.CSS_SELECTOR, "#register-confirm").click()
        except Exception as e:
            print("自动填写表单错误：")
            print(e)
            self.close()
            pass
        pass
