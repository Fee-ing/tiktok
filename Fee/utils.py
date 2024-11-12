import os
import signal
import subprocess
from time import sleep
import random
import re
import getpass
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def kill_chrome_processes():
    processes = subprocess.check_output(["ps", "aux"]).decode()
    for line in processes.split("\n"):
        if "chrome" in line or "chromedriver" in line:
            pid = int(line.split()[1])
            print(f"杀掉冲突进程 {pid}")
            os.kill(pid, signal.SIGKILL)


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


# 打开链接
def open_page(driver, url="", keys="", count=5):
    driver.get(url)

    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, keys))
        )
        return True
    except Exception as e:
        count = count - 1
        if count > 0:
            return open_page(driver, url=url, keys=keys, count=count)
        else:
            print("打开链接失败")
            return False


def prompt_username_password():
    u = input("账号: ")
    p = getpass.getpass(prompt="密码: ")
    return (u, p)


def login(driver, username=None, password=None):
    if not username or not password:
        username, password = prompt_username_password()

    driver.get("https://www.tiktok.com")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "header-login-button"))
    )

    # 点击登录
    print("点击登录按钮")
    login_button = driver.find_element(By.ID, "header-login-button")
    login_button.click()

    title_elem = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "login-modal-title"))
    )

    _sleep(5, 10)
    print("点击手机/邮箱/用户名登录")
    next_sibling = title_elem.find_element(By.XPATH, "./following-sibling::*[1]")

    # 点击手机/邮箱登录
    button_elems = next_sibling.find_elements(By.XPATH, "./child::div")
    button_elems[1].click()

    _sleep(5, 10)

    # 切换邮箱登录
    print("切换邮箱登录")
    form_elem = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#loginContainer form"))
    )
    a_elem = form_elem.find_element(By.TAG_NAME, "a")
    a_elem.click()
    _sleep(5, 10)

    # 输入邮箱、密码
    print("输入账户、密码")
    form_elem = driver.find_element(By.CSS_SELECTOR, "#loginContainer form")
    username_input = form_elem.find_element(By.XPATH, ".//input[@name='username']")
    username_input.send_keys(username)

    password_input = form_elem.find_element(By.XPATH, ".//input[@type='password']")
    password_input.send_keys(password)

    _sleep(5, 10)

    # 确认登录
    print("确认登录")
    submit_button = form_elem.find_element(By.XPATH, ".//button[@type='submit']")
    submit_button.click()

    try:
        print("登录验证中...")
        WebDriverWait(driver, 3600).until(
            EC.presence_of_element_located(
                (By.XPATH, ".//dev[@data-e2e='upload-icon']")
            )
        )
        print("登录成功")
        _sleep(5, 10)
        return True
    except Exception as e:
        print("登录失败")
        return False


def login_with_cookie(
    driver=None, cookie_session_id="", cookie_sign="", user_session=""
):
    if driver:
        driver.get("https://www.tiktok.com/explore")

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
