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


account = "user5302058888804|@K4aEsi@D5wZ|"
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


def login(driver, account=None, password=None):
    if not account or not password:
        account, password = __prompt_email_password()

    driver.get("https://www.tiktok.com/explore")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "header-login-button")))

    login_button = driver.find_element(By.ID, "header-login-button")
    login_button.click()


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

        login(driver, account, password)

    finally:
        pass
        # if driver is not None:
        #     driver.quit()


if __name__ == "__main__":
    main()
