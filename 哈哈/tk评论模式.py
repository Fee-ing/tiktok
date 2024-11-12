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

    print('检查登录 end')
    return


# 搜索操作
def search(driver):
    print('搜索 start')
    time.sleep(1)
    t = int(time.time() * 1000)
    txt = 'panda'
    driver.get(f'https://www.tiktok.com/search?q={txt}&t={t}')
    time.sleep(3)
    print('搜索 end')
    return driver


# 点击搜索的视频操作
def click(driver):
    print('点击视频 start')
    time.sleep(1)
    # 1、获取所有的href链接
    # 2、然后循环点击链接所在的a标签
    content = driver.find_elements(By.CSS_SELECTOR, '[data-e2e="search_top-item"]')
    for value in content:
        print(value)
        # 点击打开视频
        value.click()
        time.sleep(1)
        # 添加视频一级评论
        time.sleep(1)
        print('视频一级评论 start')
        # 先定位到底部
        content = driver.find_element(By.CLASS_NAME, '.css-19hqadz-DivBottomCommentContainer.e1mecfx04')
        print('视频一级评论 1')
        # 然后定位输入框
        content = content.find_element(By.CLASS_NAME, '.notranslate.public-DraftEditor-content')
        print('视频一级评论 2')
        time.sleep(1)
        content.click()
        print('视频一级评论 3')
        time.sleep(1)
        content.send_keys('Very interesting')
        print('视频一级评论 4')
        time.sleep(1)
        content.send_keys(Keys.RETURN)  # 模拟回车操作
        break
    print('点击视频 stop')


# 视频一级评论
def review(driver):
    time.sleep(1)
    print('视频一级评论 start')
    # 先定位到底部
    content = driver.find_element(By.CLASS_NAME, 'css-19hqadz-DivBottomCommentContainer e1mecfx04')
    print('视频一级评论 1')
    # 然后定位输入框
    content = content.find_element(By.CLASS_NAME, 'notranslate public-DraftEditor-content')
    print('视频一级评论 2')
    time.sleep(1)
    content.click()
    print('视频一级评论 3')
    time.sleep(1)
    content.send_keys('Very interesting')
    print('视频一级评论 4')
    time.sleep(1)
    content.send_keys(Keys.RETURN)  # 模拟回车操作

    print('视频一级评论 end')


def run():
    # 初始化
    driver = initialize()
    # 判断登录是否完成。判断是否进入首页，是否有头像模块
    check_login(driver)
    # 搜索
    search(driver)
    # 点击
    click(driver)


# wen1111lei@163.com、w3597135lei
run()
