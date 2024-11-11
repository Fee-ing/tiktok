from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
import getpass
from time import sleep
import os
import signal
import subprocess
import re
import random


test_file = "/Users/BGZB002/Downloads/test.mp4"


def kill_chrome_processes():
    processes = subprocess.check_output(["ps", "aux"]).decode()
    for line in processes.split("\n"):
        if "chrome" in line or "chromedriver" in line:
            pid = int(line.split()[1])
            print(f"杀掉冲突进程 {pid}")
            os.kill(pid, signal.SIGKILL)


def prompt_username_password():
    u = input("账号: ")
    p = getpass.getpass(prompt="密码: ")
    return (u, p)


def _sleep(min, max):
    random_number = random.randint(min, max)
    print(f"随机等待{random_number}秒")
    sleep(random_number)


def extract_digits(s):
    # 使用正则表达式匹配所有的数字
    return re.findall(r"\d+", s)


# 获取特定节点
def get_nodes_by_classname(driver, tag_name, class_name):
    all_elements = driver.find_elements(By.TAG_NAME, tag_name)
    list = []
    for element in all_elements:
        if class_name in element.get_attribute("class"):
            list.append(element)
    return list


def login_with_cookie(driver):
    driver.get("https://www.tiktok.com/")

    print("cookie登录")
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "sessionid",
            "value": "ac8153a7115b54e56a9e8e2e425fe21b",
        }
    )
    driver.add_cookie(
        {"domain": ".tiktok.com", "name": "tt-target-idc", "value": "useast5"}
    )
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "tt-target-idc-sign",
            "value": "BMOcfZyB9BpOozH-hphKBvR9CYESJNS9EEGu5--qVB1MLx9ZciphYOvuaStTQLrASWtWNW8uIBA5t98D_sDuy3GlmndcFiAxxXv3Bv9ZDrGvkVW9k_N3NKC9eFaq8aA_EuKpLnFRy0EZ2CA9WbVtNXbfBSsyN5JaJTkUkOWHh8fAT0tIDAk6wqe8RXuydCN5SvgivFaabYkzr-MLKI7hQMykySEtY0HoodWv5dKPQzghA21B3NkF8-Te-iC-t3RDnrYwezDSaq7crwRiiRsacrDk1teuQUeYapMxJG4Q_69UeW_-Us6BhCAvDEp6ISearFHAN7HxQffl5gZZd6BwN46j_DhU-53DSEShOD-9OuJ0wqU9n91j65hbSU0Gs9HMVItWBEO89lGPyt2jI3RZ6SfArSBmvYZyYWCjvEhxq7Z6SH66QwwmWFhWGMhWbKgdW5tyMNA0Mca9FQggTdfQsej8ehlsdKQdnv1EdGYbCYQ5jy7_AYn3J_AhBywSO_kA",
        }
    )

    key = "user_session"
    value = '{"uid":"7405946633051522091","lastUpdated":"1731290493517"}'
    driver.execute_script(f"window.sessionStorage.setItem('{key}', '{value}')")

    _sleep(5, 10)


def open_detail(driver, reply_link="", count=5):
    print("打开上传视频")
    driver.get(reply_link)

    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, ".//input[@type='file']"))
        )
        return True
    except Exception as e:
        count = count - 1
        if count > 0:
            return open_detail(driver, reply_link=reply_link, count=count)
        else:
            print("打开上传视频失败")
            return False


def post_video(driver, file=""):
    is_open_success = open_detail(
        driver,
        reply_link="https://www.tiktok.com/tiktokstudio/upload?from=upload",
        count=5,
    )
    if is_open_success == False:
        return

    _sleep(5, 10)

    upload_element = driver.find_element(By.XPATH, ".//input[@type='file']")
    upload_element.send_keys(file)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "uploading-info"))
    )
    print("正在上传视频中")

    WebDriverWait(driver, 3600).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-info"))
    )
    print("上传视频成功")

    _sleep(5, 10)

    print("发布视频")
    submit_button = driver.find_element(
        By.XPATH, ".//button[@data-e2e='post_video_button']"
    )
    submit_button.click()

    WebDriverWait(driver, 3600).until(
        EC.presence_of_element_located((By.CLASS_NAME, "common-modal-confirm-modal"))
    )
    print("发布成功")

    _sleep(5, 10)


def main():
    kill_chrome_processes()

    try:
        # 配置Chrome选项
        chrome_options = Options()
        # 启动无痕模式
        chrome_options.add_argument("--incognito")
        # 设置代理服务器信息
        # proxy_server = 'http://127.0.0.1:7890'
        # chrome_options.add_argument(f'--proxy-server={proxy_server}')
        # 设置ChromeDriver的路径
        # service = Service(executable_path="/usr/local/bin/chromedriver")
        service = Service()
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)

        login_with_cookie(driver)

        post_video(driver, file=test_file)

    finally:
        print("运行结束")
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
