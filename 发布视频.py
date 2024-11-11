from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import requests
import getpass
from time import sleep
import os
import signal
import subprocess
import re
import random


username = "user7399076925301"  # 用户名
cookie_session_id = "ac8153a7115b54e56a9e8e2e425fe21b"  # cookie中的sessionid
# cookie中的tt-target-idc-sign
cookie_sign = "BMOcfZyB9BpOozH-hphKBvR9CYESJNS9EEGu5--qVB1MLx9ZciphYOvuaStTQLrASWtWNW8uIBA5t98D_sDuy3GlmndcFiAxxXv3Bv9ZDrGvkVW9k_N3NKC9eFaq8aA_EuKpLnFRy0EZ2CA9WbVtNXbfBSsyN5JaJTkUkOWHh8fAT0tIDAk6wqe8RXuydCN5SvgivFaabYkzr-MLKI7hQMykySEtY0HoodWv5dKPQzghA21B3NkF8-Te-iC-t3RDnrYwezDSaq7crwRiiRsacrDk1teuQUeYapMxJG4Q_69UeW_-Us6BhCAvDEp6ISearFHAN7HxQffl5gZZd6BwN46j_DhU-53DSEShOD-9OuJ0wqU9n91j65hbSU0Gs9HMVItWBEO89lGPyt2jI3RZ6SfArSBmvYZyYWCjvEhxq7Z6SH66QwwmWFhWGMhWbKgdW5tyMNA0Mca9FQggTdfQsej8ehlsdKQdnv1EdGYbCYQ5jy7_AYn3J_AhBywSO_kA"
user_session = '{"uid":"7405946633051522091","lastUpdated":"1731290493517"}'    # session中的user_session


user_avatar = "/Users/BGZB002/Downloads/images.jpg"  # 头像
user_nickname = "Be Yourself"  # 昵称
user_desc = "be rich"  # 描述

time_interval = 1  # 间隔时间，单位分钟

post_list = [
    {"file": "/Users/BGZB002/Downloads/test.mp4", "desc": "incredible"},
    {"file": "/Users/BGZB002/Downloads/test1.mp4", "desc": "lol"},
]


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
        {"domain": ".tiktok.com", "name": "tt-target-idc", "value": "useast5"}
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


# 打开个人主页
def open_user(driver, count=5):
    print("打开个人主页")
    driver.get("https://www.tiktok.com/@" + username)

    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.XPATH, ".//button[@data-e2e='edit-profile-entrance']")
            )
        )
        return True
    except Exception as e:
        count = count - 1
        if count > 0:
            return open_user(driver, count=count)
        else:
            print("打开个人主页失败")
            return False


# 打开发布页
def open_post(driver, count=5):
    print("打开上传视频")
    driver.get("https://www.tiktok.com/tiktokstudio/upload?from=upload")

    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, ".//input[@type='file']"))
        )
        return True
    except Exception as e:
        count = count - 1
        if count > 0:
            return open_post(driver, count=count)
        else:
            print("打开上传视频失败")
            return False


# 判断头像是否上传成功
def is_save_avatar_success(driver):
    list = get_nodes_by_classname(driver, "div", "DivZoomArea")
    if len(list) > 0:
        sleep(3)
        return is_save_avatar_success(driver)
    else:
        return


# 判断保存个人信息是否更新成功
def is_save_user_info_success(driver, class_name=""):
    try:
        popup_element = driver.find_element(
            By.XPATH, f".//div[@data-e2e='{class_name}']"
        )
        sleep(3)
        return is_save_user_info_success(driver)
    except NoSuchElementException:
        return True


# 修改个人主页
def update_user_info(driver, avatar="", nickname="", desc=""):
    is_open_success = open_user(
        driver,
        count=5,
    )
    if is_open_success == False:
        return

    _sleep(5, 10)

    print("点击编辑主页")
    edit_element = driver.find_element(
        By.XPATH, ".//button[@data-e2e='edit-profile-entrance']"
    )
    edit_element.click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//div[@data-e2e='edit-profile-popup']")
        )
    )

    _sleep(5, 10)

    name_input_wrapper = driver.find_element(
        By.XPATH, ".//div[@data-e2e='edit-profile-name-input']"
    )
    try:
        name_input = name_input_wrapper.find_element(By.TAG_NAME, "input")
        print("输入昵称")
        name_input.clear()
        sleep(1)
        name_input.send_keys(nickname)

        _sleep(5, 10)
    except NoSuchElementException:
            pass

    print("输入个人介绍")
    desc_input = driver.find_element(
        By.XPATH, ".//textarea[@data-e2e='edit-profile-bio-input']"
    )
    desc_input.clear()
    sleep(1)
    desc_input.send_keys(desc)

    _sleep(5, 10)

    print("上传头像")
    upload_element = driver.find_element(By.XPATH, ".//input[@type='file']")
    upload_element.send_keys(avatar)
    sleep(3)
    popup_element = driver.find_element(
        By.XPATH, ".//div[@data-e2e='edit-profile-popup']"
    )
    all_buttons = popup_element.find_elements(By.TAG_NAME, "button")
    button_list = all_buttons[::-1]
    for button in button_list:
        if button.text == "应用":
            button.click()
            break
    is_save_avatar_success(driver)

    _sleep(5, 10)

    print("保存修改")
    save_btn = driver.find_element(By.XPATH, ".//button[@data-e2e='edit-profile-save']")
    # 检查按钮是否有 disabled 属性
    is_disabled = save_btn.get_attribute("disabled") is not None

    if is_disabled:
        print("保存失败")
    else:
        save_btn.click()

        sleep(3)

        is_save_user_info_success(driver, class_name="edit-profile-popup")

        try:
            confirm_element = driver.find_element(
                By.XPATH, ".//button[@data-e2e='set-username-popup-confirm']"
            )
            confirm_element.click()
            print("确认修改昵称")

            is_save_user_info_success(driver, class_name="set-username-popup")

        except NoSuchElementException:
            pass

        print("保存成功")

        _sleep(30, 60)


# 发布视频
def post_video(driver, file="", desc=""):
    is_open_success = open_post(
        driver,
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

    print("输入视频描述")
    input_element = driver.find_element(By.XPATH, ".//div[@contenteditable='true']")
    input_element.click()
    sleep(1)
    driver.execute_script(
        """
        var element = arguments[0];
        element.focus();
        document.execCommand('selectAll', false, null);
    """,
        input_element,
    )
    sleep(1)
    input_element.send_keys(Keys.BACKSPACE)
    sleep(1)
    input_element.send_keys(desc)

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
        service = Service(executable_path="/usr/local/bin/chromedriver")
        # service = Service()
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)

        login_with_cookie(driver)

        update_user_info(driver, avatar=user_avatar, nickname=user_nickname, desc=user_desc)

        for item in post_list:
            post_video(driver, file=item["file"], desc=item["desc"])
            print(f"等待{time_interval}分钟")
            sleep(time_interval * 60)

    finally:
        print("运行结束")
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
