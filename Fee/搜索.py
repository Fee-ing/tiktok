from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
import urllib.parse
import re
from utils import (
    kill_chrome_processes,
    _sleep,
    get_nodes_by_classname,
    extract_digits,
    open_page,
    login,
    login_with_cookie,
)


keyword = "狗"


def wait_captcha_verify(driver):
    try:
        element = driver.find_element(By.CLASS_NAME, "captcha-verify-container")
        print("图形验证中")
        sleep(60)
        wait_captcha_verify(driver)
    except NoSuchElementException:
        pass


def scroll_loop(driver, id_list=[]):
    _sleep(30, 60)

    list = driver.find_elements(By.XPATH, ".//div[@data-e2e='search_top-item']")
    count = 0
    for item in list:
        url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        # 这里可以上报链接
        print(url)
        pattern = r"^https://www\.tiktok\.com/"
        id = re.sub(pattern, "", url)

        if (id in id_list) == False:
            count = count + 1
            id_list.append(id)

    if count == 0:
        print("滚动到底部")
        return
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        id_list = id_list[-40:]
        scroll_loop(driver, id_list=id_list)


def search(driver, keyword=""):
    link = f"https://www.tiktok.com/search?q={urllib.parse.quote_plus(keyword)}&t={int(time() * 1000)}"
    print(link)

    print("打开搜索结果")
    is_open_success = open_page(
        driver, url=link, keys=".//div[@data-e2e='search_top-item']"
    )
    if is_open_success == False:
        return

    scroll_loop(driver, id_list=[])


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

        # is_login_success = login(driver, username, password)
        # if is_login_success == False:
        #     return

        search(driver, keyword=keyword)

    finally:
        print("运行结束")
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
