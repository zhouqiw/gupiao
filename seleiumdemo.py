# encoding: utf-8

"""
@author: zhouqi
@software: PyCharm
@file: seleiumdemo.py
@time: 2018/11/11 上午11:10
"""
import time
from selenium import webdriver
driver = webdriver.Chrome()
# driver.get("https://www.google.com")
# e = driver.find_element_by_link_text('English')
# e.click()
# q = driver.find_element_by_name('q')
# q.send_keys("english")
# driver.close()
driver.get("http://www.baidu.com/")
driver.find_element_by_id("kw").clear()
driver.find_element_by_id("kw").send_keys("python")
driver.find_element_by_id("form").submit()
p0 = driver.title
# driver.find_element_by_link_text(u"体验Python语言编程 - 下载PyCharm智能集成开发工具").click()
driver.find_element_by_xpath('//*[@id="1"]/div[2]').click()
time.sleep(5)
driver.switch_to_window(p0)
# ERROR: Caught exception [ERROR: Unsupported command [selectWindow | win_ser_1 | ]]
driver.close()
time.sleep(10)
driver.close()
