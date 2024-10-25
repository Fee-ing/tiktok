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


username = "user5302058888804|@K4aEsi@D5wZ|"
password = "canicamboya80@hotmail.com|e5WpgspM"


def kill_chrome_processes():
    processes = subprocess.check_output(["ps", "aux"]).decode()
    for line in processes.split("\n"):
        if "chrome" in line or "chromedriver" in line:
            pid = int(line.split()[1])
            print(f"Killing process {pid}")
            os.kill(pid, signal.SIGKILL)

def __prompt_email_password():
    u = input("账号: ")
    p = getpass.getpass(prompt="密码: ")
    return (u, p)


def login(driver, username=None, password=None):
    if not username or not password:
        username, password = __prompt_email_password()

    driver.get("https://www.tiktok.com/explore")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "header-login-button")))

    login_button = driver.find_element(By.ID, "header-login-button")
    login_button.click()

    title_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-modal-title"))
    )

    next_sibling = title_elem.find_element(By.XPATH, './following-sibling::*[1]')

    button_elems = next_sibling.find_elements(By.XPATH, "./child::div")
    button_elems[1].click()

    sleep(2)

    form_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#loginContainer form"))
    )
    a_elem = form_elem.find_element(By.TAG_NAME, 'a')
    a_elem.click()
    sleep(2)

    username_input = form_elem.find_element(By.XPATH, ".//input[@name='username']")
    username_input.send_keys(username)

    password_input = form_elem.find_element(By.XPATH, ".//input[@type='password']")
    password_input.send_keys(password)

    sleep(3600)


def main():
    kill_chrome_processes()

    try:
        # 配置Chrome选项
        chrome_options = Options()
        # 设置代理服务器信息
        proxy_server = "http://127.0.0.1:7890"
        chrome_options.add_argument(f"--proxy-server={proxy_server}")
        # 设置ChromeDriver的路径
        service = Service(executable_path="/usr/local/bin/chromedriver")
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)

        login(driver, username, password)

    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
