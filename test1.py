import task
import bili_utils
from selenium import  webdriver
import os

username=""   #your username
password=""   #your password

driver=webdriver.Chrome()

if not os.path.isfile("bili_login.json"):
    bili_utils.login_and_get_cookie(driver,"https://www.bilibili.com/",username,password)
t=task.Task()
#t.spawn_all_task()
t.load_from_file()
t.print_info()
t.make_thread(["key"],headless=False,limit=20,page=5)   #replace key with your keyword