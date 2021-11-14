# SignUper
## 运行环境

- 操作系统：Centos7 或Mac OS(已经测试)
- 安装Chrome并下载好chromedirver
- 安装好扩展库
## 安装
首先安装Google Chrome浏览器和Selenium扩展安装方法请参考：

[Centos7-安装Chrome无GUI运行selenium-chromedriver](https://pgw1315.github.io/2021/11/03/Centos7-安装Chrome无GUI运行selenium-chromedriver/)
### 安装扩展库
```bash 
pip3 install selenium
pip3 install Pillow
pip3 install requests
```

## 使用

```bash 
python3 main.py
python3 Refresh.py
```
## 添加计划任务
```bash 
vim /etc/crontab
```
```bash 
*/5 * * * * root cd /www/code/SignUper && PYTHONIOENCODING=utf-8 /usr/bin/python3 Refresh.py >> logs/refresh.log 2>&1
5,32 * * * * root cd /www/code/SignUper && PYTHONIOENCODING=utf-8 /usr/bin/python3 main.py >> logs/reg.log 2>&1
```