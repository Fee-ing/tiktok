from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


# 初始化
def initialize():
    chrome_options = Options()
    # 1、创建一个Chrome的无头浏览器
    # chrome_options.add_argument("--headless")  # 无头模式(没有html页面)
    chrome_options.add_argument("--incognito")  # 无痕模式
    # 2、浏览器设置常开，不自动关闭
    chrome_options.add_experimental_option("detach", True)
    # 3、设置浏览器路径
    chrome_options.binary_location = './Chrome/chrome.exe'
    # 4、设置浏览器驱动路径
    ser = Service()
    ser.executable_path = './chromedriver/chromedriver.exe'
    # 唤起浏览器
    driver = webdriver.Chrome(options=chrome_options, service=ser)
    driver.get('https://www.tiktok.com/explore')
    time.sleep(2)
    return driver


# 判断登录是否完成。判断是否进入首页，是否有中文“我”
def check_login(driver):
    # 判断id元素是否存在，存在就往下走（创建一个等待对象，等待时间不超过20秒，每1秒检查一次 ）
    print('检查登录 start')
    i = 0
    while 1:
        html = driver.page_source  # 获取网页源代码
        soup = BeautifulSoup(html, 'html.parser')  # 使用html.parser解析HTML
        content = soup.find(class_="css-1deszxq-DivHeaderInboxContainer e18kkhh40")  # 检测头像框是否存在
        if content:
            print(f'{i}已登录')
            time.sleep(2)
            break
        else:
            print(f'{i}未登录')  # 继续循环等待
            time.sleep(1)
        i = i + 1
    print('登录成功')
    return


def run():
    # 初始化
    driver = initialize()
    # 判断登录是否完成。判断是否进入首页，是否有头像模块
    check_login(driver)


run()
