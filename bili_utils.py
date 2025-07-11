import time

import selenium
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import json
from pywinauto.application import Application


def login_and_get_cookie(driver, url, username: str, password: str):
    driver.get(url)
    login_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div/div/span')
    login_button.click()
    time.sleep(5)
    # print(driver.find_element(By.CSS_SELECTOR,"div.login-pwd-wp > form > div:nth-child(3)").get_attribute('outerHTML'))
    username_input = driver.find_element(By.CSS_SELECTOR, 'div.login-pwd-wp > form > '
                                                          'div:nth-child(1) > input')
    password_input = driver.find_element(By.CSS_SELECTOR, 'div.login-pwd-wp > form > '
                                                          'div:nth-child(3) > input')
    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'div.login-pwd-wp > div.btn_wp > div.btn_primary').click()
    time.sleep(30)
    cookies = driver.get_cookies()
    with open('bili_login.json', 'w') as f:
        json.dump(cookies, f)
    driver.quit()
    time.sleep(5)


def inject_cookie_and_login(driver, url):
    driver.get(url)
    cookies = None
    with open('bili_login.json', 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)


def search(driver, keyword: str):
    searchbar = driver.find_element(By.CSS_SELECTOR, "input.nav-search-input")
    searchbar.send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR, "div.nav-search-btn").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.CSS_SELECTOR, "div.conditions-order.flex_between > div > button:nth-child(3)").click()

def change_page(driver):
    buttons=driver.find_elements(By.CSS_SELECTOR,"button.vui_pagenation--btn-side")
    driver.execute_script("arguments[0].scrollIntoView();", buttons[1])
    buttons[1].click()

def get_comment_box(driver):
    comment_box = driver.execute_script('var host=document.querySelector("bili-comments");'
                                        'host=host.shadowRoot;'
                                        'host=host.querySelector("bili-comments-header-renderer");'
                                        'host=host.shadowRoot;'
                                        'host=host.querySelector("bili-comment-box");'
                                        'return host;')
    return comment_box


def get_edt(driver, parent=None):
    comment_box = parent
    if not parent:
        comment_box = driver.execute_script('var host=document.querySelector("bili-comments");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comments-header-renderer");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comment-box");'
                                            'return host;')
    edt = driver.execute_script('var host=arguments[0].shadowRoot;'
                                'host=host.querySelector("bili-comment-rich-textarea");'
                                'host=host.shadowRoot;'
                                'var temp=host.querySelector("div.brt-editor");'
                                'return temp;', comment_box)
    return edt


def send_message(edt, message):
    edt.click()
    edt.send_keys(message)


def at_choose(driver, parent=None):
    comment_box = parent
    if not parent:
        comment_box = driver.execute_script('var host=document.querySelector("bili-comments");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comments-header-renderer");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comment-box");'
                                            'return host;')
    at_choice = driver.execute_script('var host=arguments[0].shadowRoot;'
                                      'host=host.querySelector("bili-comment-mention-popover");'
                                      'host=host.shadowRoot;'
                                      'var result=host.querySelector("li:nth-child(1)");'
                                      'return result', comment_box)
    at_choice.click()


def get_img_btn(driver,parent=None):
    comment_box = parent
    if not parent:
        comment_box = driver.execute_script('var host=document.querySelector("bili-comments");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comments-header-renderer");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comment-box");'
                                            'return host;')
    img = driver.execute_script('var host=arguments[0].shadowRoot;'
                                'host=host.querySelector("button:nth-child(4)");'
                                'host=host.querySelector("bili-icon");'
                                'return host', comment_box)
    return img

def img_dialog(img_btn, img_path, window_var=None):
    if window_var is None:
        window_var = ["Open", "Open", "Edit", "Open"]
    img_btn.click()
    time.sleep(5)

    app = Application().connect(title_re=window_var[0])
    dialog = app.window(title_re=window_var[1])
    dialog[window_var[2]].type_keys(img_path)
    dialog[window_var[3]].click()


def cycle(driver, keyword, messages, limit=10,page=1):
    search(driver, keyword)
    temp = driver.find_element(By.CSS_SELECTOR, "div.video-list.row")
    driver.execute_script("arguments[0].scrollIntoView();", temp)
    time.sleep(5)
    for p in range(page):
        print("+++++++++++++++++++++++++++++++++")
        print(p)
        driver.switch_to.window(driver.window_handles[1])
        if p>0:
            change_page(driver)
            time.sleep(5)
        for i in range(limit):
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)
            temp = driver.find_element(By.CSS_SELECTOR, "div.video-list.row")
            vid_list = temp.find_elements(By.CSS_SELECTOR, 'div.bili-video-card')
            vid = vid_list[i]
            print(i + 1)
            print(vid.find_element(By.CSS_SELECTOR, 'img').get_attribute('outerHTML'))
            print("===================================")
            try:
                driver.execute_script("arguments[0].scrollIntoView();", vid)
                vid.click()
            except:
                continue
            time.sleep(3)

            driver.switch_to.window(driver.window_handles[2])
            time.sleep(3)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)
            for m in messages:
                try:
                    comment_box = get_comment_box(driver)
                    edt = get_edt(driver, comment_box)
                    driver.execute_script("arguments[0].scrollIntoView();", edt)
                    edt.send_keys(m[0])
                    if m[1]:
                        time.sleep(3)
                        at_choose(driver, comment_box)
                    if len(m[2]):
                        img_btn=get_img_btn(driver,comment_box)
                        img_dialog(img_btn,m[2])
                    time.sleep(20)
                    driver.execute_script('var host=arguments[0].shadowRoot;'
                                          'host.querySelector("div#pub > button").click();', comment_box)
                except Exception as e:
                    print(e)
                time.sleep(5)
            driver.close()
    driver.quit()


def vid(driver, message, count):
    temp = driver.find_element(By.CSS_SELECTOR, "div.video-list.row")
    driver.execute_script("arguments[0].scrollIntoView();", temp)
    time.sleep(5)
    for i in range(count):
        print(i)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        temp = driver.find_element(By.CSS_SELECTOR, "div.video-list.row")
        vid_list = temp.find_elements(By.CSS_SELECTOR, 'div.bili-video-card')
        vid = vid_list[i]
        print(vid.find_element(By.CSS_SELECTOR, 'img').get_attribute('outerHTML'))
        vid.click()
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[2])
        time.sleep(3)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        comment_box = driver.execute_script('var host=document.querySelector("bili-comments");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comments-header-renderer");'
                                            'host=host.shadowRoot;'
                                            'host=host.querySelector("bili-comment-box");'
                                            'return host;')
        print(comment_box.get_attribute('outerHTML'))
        edt = driver.execute_script('var host=arguments[0].shadowRoot;'
                                    'host=host.querySelector("bili-comment-rich-textarea");'
                                    'host=host.shadowRoot;'
                                    'var temp=host.querySelector("div.brt-editor");'
                                    'return temp;', comment_box)
        img = driver.execute_script('var host=arguments[0].shadowRoot;'
                                    'host=host.querySelector("button:nth-child(4)");'
                                    'host=host.querySelector("bili-icon");'
                                    'return host', comment_box)
        for m in message:
            try:
                edt.click()
                edt.send_keys(m)
                driver.execute_script('var host=arguments[0].shadowRoot;'
                                      'host.querySelector("div#pub > button").click();', comment_box)
                time.sleep(5)
            except Exception as e:
                print(e)
        driver.close()
    time.sleep(5)
