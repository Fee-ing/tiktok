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


test_file = "D:/project/python/tools/抖音/素材/nature.mp4"


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
            "value": "2558db1b186602e050e8824c6345fb43",  # cookie--sessionid--值
        }
    )
    driver.add_cookie(
        {"domain": ".tiktok.com", "name": "tt-target-idc", "value": "useast5"}
    )
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "tt-target-idc-sign",
            # cookie--tt-target-idc-sign--值
            "value": "rDmEeAUqH_tgi1JbDMrkH7Z1Otbo4_njHN6zzrjOduAF1IaPXGh26XNVBPaMfZF30Xllrx8aq0izIxyxn4-fc-pP_MMAftdloA_OUhs-4yZtbdTc8kPpko4cV-0r25LMduoR52R3x2eru5GlhAV-VWhMGEQfKpR5jZ24EZx5Lob74-sohMZ-Z9DzYefSW3IlPsYmTlfku2MeILMuwtwNVj6ly4V0DP1aaoH3zFWo3itVycbFajpC6NGYT4pcnsYE1CyEjE5Drr1eF4TcEN3UBgRU1FgDjjhjzGSvMWrRiwQ_mC-5i5fHtYO-Cr8IQSUF9xyUDUKkJHDipPMf2pTAt2t4lUTKVQz84zeMWCz8umw78K6hyy_Vs93MRPLkxZvHf_YpeQuxO6RvEjCX8l6A5-nKBCwXYV3fHZM71jQzJjYgY_vZHJpPSTEdbbPz69g4yXxgjMMuefpikEDvW2OJMJY_xigCgIx5K4ayKtM60JHQYmG6T0Hyx_Q285ET4R5S",
        }
    )

    key = "user_session"
    # 会话存储空间（session storage）--user_session--值
    value = '{"uid":"7405973899005838382","lastUpdated":"1731302263198"}'
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
    # kill_chrome_processes()

    try:
        # 配置Chrome选项
        chrome_options = Options()
        # 启动无痕模式
        chrome_options.add_argument("--incognito")
        # 2、浏览器设置常开，不自动关闭
        chrome_options.add_experimental_option("detach", True)
        # 设置代理服务器信息
        # proxy_server = 'http://127.0.0.1:7890'
        # chrome_options.add_argument(f'--proxy-server={proxy_server}')
        # 设置ChromeDriver的路径
        service = Service(executable_path="./chromedriver/chromedriver.exe")
        # service = Service()
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
