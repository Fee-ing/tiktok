from selenium import webdriver
#from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType

import re
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import requests
import os
import subprocess
import signal
from configparser import ConfigParser

from tiktok_captcha_solver import SeleniumSolver
import undetected_chromedriver as uc

import socket

import urllib.parse
from time import sleep, time
from datetime import datetime, timedelta

from utils import (
    kill_chrome_processes,
    _sleep,
    get_nodes_by_classname,
    extract_digits,
    open_page,
    login,
    #login_with_cookie,
)

keyword = "韩国"
parserUrl = 'https://www.tiktok.com/@aespa_official/video/7434103235100642578'

test_reply = "I can watch it all day!"

comment_keywords = ["panda", "cute", "Kung Fu", "kungfu"]

username = "user7399076925301"
password = "@K4axNj6w@qo"

api_key = "4a819db52a2fd25362c2a37ab20b570a"
cookie_session_id = "8d329519f04830818c87c507b5aa2d88"  # cookie中的sessionid
# cookie中的tt-target-idc-sign
#tt-target-idc
cookie_sign = "Dty1sAkG0Q2gEq-J76eDk6w14kLj0CXy8GKyvuqTQ0QI5p7-rujsYrxA5iVqNI8G9TPB_T-2EQOw6bntqxaX0d-bvhP3OBrRFMaGGSxiqxf9EAQRafrv0kch9j1EEJj1MObErXySEHarL8tmOgnV1B3g_ekZbCpHYoEkuXgnCEXrQMdXXCYDKywJXPxw4HIKOHq1QxnO-tWTU2ZpyrfHqOeF_jGhie3Z_7BxwhSKUMua51idJGwE0yoi2BCKUrisWWKgm0pBA8csNTGb0wRvFmKZVrnooxtSmoR0ROYe0q3YrjUs42G65yWn57hP4YG2rGYavLunJQddPOC7a36f3q81IhLPdo6KgfWKWFN5hP8-ZM0c0iNj4Nr61LIEI8V91V33mmslP4s85H-a6Z-mpf0GcMOhUPSbrw8dJcOgFs-pQjM51fvnoKBW74rVGtodUC1w88tazBDsHBa0odAs6fXssn0FPzHr_WI84pqGuMYxraIEnRbaUv-cKeEdBaO1Dty1sAkG0Q2gEq-J76eDk6w14kLj0CXy8GKyvuqTQ0QI5p7-rujsYrxA5iVqNI8G9TPB_T-2EQOw6bntqxaX0d-bvhP3OBrRFMaGGSxiqxf9EAQRafrv0kch9j1EEJj1MObErXySEHarL8tmOgnV1B3g_ekZbCpHYoEkuXgnCEXrQMdXXCYDKywJXPxw4HIKOHq1QxnO-tWTU2ZpyrfHqOeF_jGhie3Z_7BxwhSKUMua51idJGwE0yoi2BCKUrisWWKgm0pBA8csNTGb0wRvFmKZVrnooxtSmoR0ROYe0q3YrjUs42G65yWn57hP4YG2rGYavLunJQddPOC7a36f3q81IhLPdo6KgfWKWFN5hP8-ZM0c0iNj4Nr61LIEI8V91V33mmslP4s85H-a6Z-mpf0GcMOhUPSbrw8dJcOgFs-pQjM51fvnoKBW74rVGtodUC1w88tazBDsHBa0odAs6fXssn0FPzHr_WI84pqGuMYxraIEnRbaUv-cKeEdBaO1"
user_session = '{"uid":"7436018394833814546","lastUpdated":"1731500825505"}'    # session中的user_session
headers = {
            'Connection': 'close',
        }


g_task_id = ''
g_task_type = ''
g_ke_word = ''
g_task_num = ''
g_task_count = 0
g_task_time = ''
g_ip = ''
g_from_num = ''
g_tk_account_name = ''
def senduserinfo(ip,from_num,tk_account_name,personage_name,task_id,center_url,avatar_url,comment):
    token = 'dicNvMdkiWBh2HLG0Z9ZnrkZBb'
    ip = ip
    from_num = from_num
    tk_account_name = tk_account_name
    personage_name = personage_name
    avatar = avatar_url
    review = comment
    center_url = center_url
    gender = '男'
    task_id = task_id
    msg = 0
    print('ip:',ip)
    print('from_num:', from_num)
    print('tk_account_name:', tk_account_name)
    print('personage_name:', personage_name)
    print('avatar:', avatar)
    print('review:', review)
    print('center_url:', center_url)
    print('gender:', gender)
    try:
        url_send_task = "http://38.181.47.22/py/send/user-info"
        params_send_task = {
            'token': token,
            'ip': ip,
            'from_num': from_num,
            'tk_account_name': tk_account_name,
            'personage_name': personage_name,
            'avatar': avatar,
            'review': review,
            'center_url': center_url,
            'gender': gender
        }
        print('发送视频URL开始')
        response_send = requests.post(url_send_task, data=params_send_task)
        print(response_send)
        if response_send.status_code == 200:
            print("请求成功")
            print("响应头:")
            print(response_send.headers)  # 打印响应头
            print("响应内容:")
            print(response_send.text)  # 打印文本形式的响应内容
            rs_json = response_send.json()
            r = rs_json['data']
            print('r:',r)
            if r.find('重复') != -1:
                msg = 1
            return msg
        else:
            print("请求失败，状态码:", response_send.status_code)
            msg = 2
            return msg

    except Exception as e:
        print("except:sendvideourl():", str(e))
        msg = 3
        return msg
def gettask():
    rs = 0
    task_id =''
    task_type = ''
    ke_word = ''
    task_num = ''
    task_time = ''
    video_url = ''
    try:
        url_send_task = "http://38.181.47.22/py/get/task"
        token = 'dicNvMdkiWBh2HLG0Z9ZnrkZBb'
        ip = get_ip_address()
        from_num = '1'
        tk_account_name = ''
        params_send_task = {
            'token': token,
            'ip': ip,
            'from_num': from_num,
            'tk_account_name': tk_account_name
        }
        print('获取任务开始')
        rs_task = requests.post(url_send_task, data=params_send_task)
        print('获取任务:',rs_task.json())
        rs_json_task = rs_task.json()
        msg_task = rs_json_task['msg']
        if 'ok' in msg_task:
            print('开始处理返回的任务数据')
            rs = 1
            task_id = rs_json_task['data']['task_id']
            task_type = rs_json_task['data']['type']
            ke_word = rs_json_task['data']['key_word']
            task_num = rs_json_task['data']['num']
            task_time = rs_json_task['data']['time']
            if task_type == 3:
                video_url = rs_json_task['data']['video_url']
            '''
            print('rs:',rs)
            print(task_id)
            print(task_type)
            print(ke_word)
            print(task_num)
            print(task_time)
            '''
            return rs,task_id,task_type,ke_word,task_num,task_time,video_url
        else:
            print('获取账号 失败')
            rs = 0
            return rs,task_id,task_type,ke_word,task_num,task_time,video_url
    except Exception as e:
        print("except:gettask():", str(e))
        rs = 0
        return rs, task_id, task_type, ke_word, task_num, task_time,video_url
def days_since_date(year, month, day):
    # 创建指定的日期
    specified_date = datetime(year, month, day)
    # 创建今天的日期
    today = datetime.today()
    # 计算两个日期之间的差异
    delta = today - specified_date
    # 返回总天数
    return delta.days
def get_ip_address():
    try:
        # 获取本地主机名
        hostname = socket.gethostname()
        # 获取本地IP
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        print(f"Unable to get IP Address: {e}")

def scroll_loop_commentByObjectWrapper(driver):
    _sleep(30, 60)

    list = driver.find_elements(By.CLASS_NAME, "DivCommentObjectWrapper")
    count = 0
    for item in list:
        url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(url)
        imgurl = item.find_element(By.TAG_NAME, "img").get_attribute("src")
        print(imgurl)
        count = count + 1

    if count == 0:
        print("滚动到底部")
        return
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_loop_commentByItemContainer(driver)
def scroll_loop_commentByItemContainer(driver):
    _sleep(30, 60)

    list = driver.find_elements(By.CLASS_NAME, "DivCommentItemContainer")
    count = 0
    for item in list:
        url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(url)
        imgurl = item.find_element(By.TAG_NAME, "img").get_attribute("src")
        print(imgurl)
        count = count + 1

    if count == 0:
        print("滚动到底部")
        return
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_loop_commentByItemContainer(driver)


# 用cookie登录
def login_with_cookie(driver):
    driver.get("https://www.tiktok.com/")

    print("cookie登录")
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "sessionid",
            "value": cookie_session_id,
        }
    )
    driver.add_cookie(
        {"domain": ".tiktok.com", "name": "tt-target-idc", "value": "alisg"}
    )
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "tt-target-idc-sign",
            "value": cookie_sign,
        }
    )

    driver.execute_script(
        f"window.sessionStorage.setItem('user_session', '{user_session}')"
    )

    _sleep(5, 10)

    driver.refresh()

def _captcha_solver(driver,sadcaptcha):
    rs = 0
    while 1:
        #time.sleep(5)
        _sleep(5,5)
        print('rs is:',rs)
        if rs == 2:
            break
        try:
            #//*[@id=":r4:"]/div
            #/html/body/div[9]
            #/html/body/div[9]/div  TUXModal-overlay  TUXModal.captcha-verify-container
            _captcha = driver.find_element(By.XPATH, ".//*[@class='TUXModal-overlay']")
            rs = 1
        except Exception as e:
            rs = 2
            print('rs is 2')
            return
        if rs == 1:
            sadcaptcha.solve_captcha_if_present()

# 判断评论中是否有关键词
def is_comment_have_keywords(text):
    for k in comment_keywords:
        if k in text:
            return True
    return False

# 滚动加载评论
def scroll_comment(driver, reply_type="1", reply_text="hello", id_list=[]):
    _sleep(30, 60)
    #_sleep(5, 10)
    comment_list = get_nodes_by_classname(driver, "div", "DivCommentObjectWrapper")

    if len(comment_list) == 0:
        print("当前视频暂无评论")
        return

    last_id = None
    if len(id_list) > 0:
        last_id = id_list[len(id_list) - 1]

    if len(comment_list) >= 40:
        comment_list = comment_list[-40:]

    for comment_item in comment_list:
        img_src = comment_item.find_element(By.TAG_NAME, "img").get_attribute("src")
        print('img_src:',img_src)
        # 获取评论id
        comment_name_item = comment_item.find_element(By.TAG_NAME, "a")
        comment_name = comment_name_item.find_element(By.TAG_NAME, "span").text
        print('comment_name:',comment_name)
        comment_id = comment_item.find_element(By.TAG_NAME, "a").get_attribute("href")
        comment_user_url = comment_id
        print('comment_user_url:', comment_user_url)
        pattern = r"https?://([^/]+)"
        comment_id = re.sub(pattern, "", comment_id).strip("/")
        comment_text = ''

        if (comment_id in id_list) == False and (username in comment_id) == False:
            id_list.append(comment_id)

            if "1" in reply_type:
                try:
                    p_elem = comment_item.find_element(
                        By.XPATH, ".//span[@data-e2e='comment-level-1']"
                    )
                    text = p_elem.find_element(By.TAG_NAME, "span").text
                    comment_text = text
                    print(comment_text)
                    # 判断评论中是否包含关键词
                    bol = is_comment_have_keywords(text)
                    if bol == True:
                        i =0
                        #send_message(driver, id=comment_id)

                except Exception as e:
                    pass

            if "3" in reply_type:
                i = 0
                #reply_comments_of_comment(comment_item, reply_text=reply_text)
        #ip, from_num, tk_account_name, task_id, center_url, avatar_url, comment
        senduserinfo(g_ip,g_from_num,g_tk_account_name,comment_name,g_task_id,comment_user_url,img_src,comment_text)
        _sleep(1,1)
    if last_id == id_list[len(id_list) - 1]:
        print("评论加载完毕")
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        id_list = id_list[-40:]
        scroll_comment(
            driver, reply_type=reply_type, reply_text=reply_text, id_list=id_list
        )


# 加载评论的评论
def expand_comments_of_comment(driver, num=0):
    list = get_nodes_by_classname(driver, "div", "DivViewRepliesContainer")

    if len(list) == 0:
        return

    elif len(list) == 1:
        print("展开评论")
        text = list[0].find_element(By.TAG_NAME, "span").text
        if any(char.isdigit() for char in text):
            # 避免打不开最后一条评论而陷入死循环
            arr = extract_digits(text)
            _num = int(arr[0])
            if _num == 1 and num == 1:
                return
            else:
                num = _num
                list[0].click()
                _sleep(20, 40)
        else:
            return

    elif len(list) == 2:
        print("展开评论")
        for item in list:
            text = item.find_element(By.TAG_NAME, "span").text
            if any(char.isdigit() for char in text):
                # 避免打不开最后一条评论而陷入死循环
                arr = extract_digits(text)
                _num = int(arr[0])
                if _num == 1 and num == 1:
                    return
                else:
                    num = _num
                    item.click()
                    _sleep(20, 40)
                    break

    expand_comments_of_comment(driver, num=num)
def parserPage(driver,url,sadcaptcha):
    driver.get(url)
    _sleep(5,5)
    elements = driver.find_elements(By.TAG_NAME,'video')
    for element in elements:
        driver.execute_script("arguments[0].click();", element)
    # 输出找到的元素数量
    print(f"找到 {len(elements)} video.")

    _sleep(1,1)

    _captcha_solver(driver, sadcaptcha)

    rs_find = 0
    try:
        comments = driver.find_elements(By.CLASS_NAME, "DivCommentItemContainer")
        rs_find = 1
    except Exception as e:
        rs_find = 0
        print('parserPage():',e)
    if rs_find == 0:
        try:
            comments = driver.find_elements(By.CLASS_NAME, "DivCommentItemWrapper")
            rs_find = 2
        except Exception as e:
            rs_find = 0
            print('parserPage():', e)
    if rs_find == 0:
        try:
            comments = driver.find_elements(By.CLASS_NAME, "DivCommentObjectWrapper")
            rs_find = 3
        except Exception as e:
            rs_find = 0
            print('parserPage():', e)
    print('rs_find:',rs_find)
    if rs_find == 1:
        scroll_comment(driver)
    elif rs_find == 3:
        scroll_comment(driver)
        #scroll_loop_commentByObjectWrapper(driver)


def main():
    # 创建解析器对象
    config = ConfigParser()

    # 读取配置文件
    config.read('config.ini')
    proxy = config.get('server', 'ip')
    port = config.get('server', 'port')
    type_ip = config.get('server', 'type')
    randoma = config.getint('step', 'randoma')
    randomb = config.getint('step', 'randomb')
    stepa = config.getint('step', 'stepa')
    stepb = config.getint('step', 'stepb')
    runingtime = config.getint('time', 'runingtime')
    sleeptingtime = config.getint('time', 'sleeptingtime')
    waitingtime = config.getint('time', 'waitingtime')
    xiumiantime = config.getint('time', 'xiumiantime')
    n2Exection = config.getint('excetion', 'nExection')  # 判断异常的时间

    # print('runingtime:',runingtime)
    # print('sleeptingtime',sleeptingtime)
    # print('waitingtime',waitingtime)
    # print('xiumiantime',xiumiantime)
    # print('n2Exection',n2Exection)

    # 调用函数并打印结果
    print(get_ip_address())
    rs = 0
    task_id = ''
    task_type = ''
    ke_word = ''
    task_num = ''
    task_time = ''
    video_url = ''
    print('现在使用的是临时链接，待服务器恢复后使用从服务器获得的链接。')
    ''' 待服务器恢复后恢复
    while True:
        rs, task_id, task_type, ke_word, task_num, task_time,video_url = gettask()
        if task_type.find('3') == -1:
            _sleep(1,1)
            continue
        if rs == 1:
            break
        _sleep(60,60)
    '''
    _sleep(1,1)
    print('main-rs:', rs)
    print(task_id)
    print(task_type)
    print(ke_word)
    print(task_num)
    print(task_time)
    print(video_url)

    global g_task_id
    global g_task_type
    global g_ke_word
    global g_task_num
    global g_task_time
    global g_ip
    global g_from_num
    global g_tk_account_name
    global g_task_count

    g_task_id = task_id
    g_task_type = task_type
    g_ke_word = ke_word
    g_task_num = task_num
    g_task_time = task_time
    print('g_task_time:',g_task_time)
    g_ip = get_ip_address()
    g_from_num = '1'
    g_tk_account_name = 'kk'
    g_task_count = 0

    keyword = ke_word

    chrome_options = Options()
    # 启动无痕模式
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option('detach', True)  # 不自动关闭浏览器
    # chrome_options.binary_location = r'D:\Chrome\chrome.exe'
    # 设置代理服务器信息
    proxy_server = 'http://127.0.0.1:7890'
    chrome_options.add_argument(f'--proxy-server={proxy_server}')
    # 设置ChromeDriver的路径
    ser = Service()
    # ser.executable_path = r'.\driver\chromedriver.
    ser.executable_path = r'.\driverNew\chromedriver.exe'
    print('0')
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    sadcaptcha = SeleniumSolver(driver, api_key)
    #login_with_cookie(driver)

    #time.sleep(3)
    _sleep(5,5)
    #带服务器恢复后这里要使用video_url
    #parserUrl = video_url
    print('parserUrl:',parserUrl)
    parserPage(driver,parserUrl,sadcaptcha)

    # 刷新间隔时间（秒）
    refresh_interval = 10
    while 1:
        #time.sleep(refresh_interval)
        _sleep(refresh_interval,refresh_interval)
        _captcha_solver(driver,sadcaptcha)
        #sadcaptcha.solve_captcha_if_present()

if __name__ == '__main__':
    print('开始吧,搜索个人主页内容')
    main()