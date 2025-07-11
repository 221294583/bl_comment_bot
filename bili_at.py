import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from bili_utils import *

username="1756206971"
password="hvfdcf51168"

driver=webdriver.Chrome()

if not os.path.isfile("bili_login.json"):
    login_and_get_cookie(driver,"https://www.bilibili.com/",username,password)

else:
    inject_cookie_and_login(driver,"https://www.bilibili.com/")
    time.sleep(3)
    cycle(driver,'blg',[('遛狗 @来自天际省的天时',1),(" 遛狗 @原pppp",1),(" 遛狗 @冷感猫猫",1)])
    """
    search(driver,"blg")
    vid(driver,[('@Glory丨小希',1)],20)#'遛狗 @来自天际省的天时','遛狗 @原pppp','遛狗 @冷感猫猫',
    """
    time.sleep(10)