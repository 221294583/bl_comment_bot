import json
import threading

import requests
import time
import bili_utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Task:
    def __init__(self,path='./task.json'):
        self.path=path
        self.uid_dict={}
        self.message_dict={}
        self.base_url="https://api.bilibili.com/x/web-interface/card?mid="
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.bilibili.com/",
        }

    def spawn_all_task(self,message="@{name}"):
        with open(self.path,'r',encoding='utf-8') as f:
            self.uid_dict=json.load(f)
        for key in self.uid_dict.keys():
            for uid in self.uid_dict[key]:
                try:
                    temp_url=self.base_url+str(uid[0])
                    response=requests.get(temp_url,headers=self.headers)
                    print(temp_url)
                    print(response)
                    if response.status_code==200:
                        print(response.json())
                        buffer=response.json()
                        buffer=buffer["data"]
                        buffer=buffer["card"]
                        self.message_dict.setdefault(key,[]).append([message.format(**buffer),uid[1],""])
                    print("++++++++++++++++++")
                except Exception as e:
                    print(e)

    def load_from_file(self,file='./task_re.json'):
        with open(file, 'r',encoding='utf-8') as f:
            self.message_dict=json.load(f)

    def print_info(self):
        print(self.uid_dict)
        print(self.message_dict)

    def get_message_dict(self):
        return self.message_dict

    def save_task(self):
        with open('task_re.json', 'w', encoding='utf-8') as f:
            json.dump(self.message_dict,fp=f,ensure_ascii=False)

    def remove_group(self,keys):
        for key in keys:
            if key in self.message_dict:
                del self.message_dict[key]

    def set_group(self,key,value):
        self.message_dict[key]=value

    def make_thread(self,keys,headless=False,limit=20,page=1):
        threads=[]
        for key in keys:
            op=Options()
            if headless:
                op.add_argument("--headless")
            driver=webdriver.Chrome(options=op)
            bili_utils.inject_cookie_and_login(driver, "https://www.bilibili.com/")
            time.sleep(3)
            t=threading.Thread(target=bili_utils.cycle,args=(driver,key,self.message_dict[key],limit,page))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
