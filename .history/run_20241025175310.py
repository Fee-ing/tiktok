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


username = "user7399076925301"
password = "@K4axNj6w@qo"
search_keywords = ["熊猫"]
comment_keywords = ["panda", "cute"]

# username = 'user5302058888804'
# password = '@K4aEsi@D5wZ'


def kill_chrome_processes():
    processes = subprocess.check_output(["ps", "aux"]).decode()
    for line in processes.split("\n"):
        if "chrome" in line or "chromedriver" in line:
            pid = int(line.split()[1])
            print(f"Killing process {pid}")
            os.kill(pid, signal.SIGKILL)


def prompt_email_password():
    u = input("账号: ")
    p = getpass.getpass(prompt="密码: ")
    return (u, p)

def _sleep(min, max):
    random_number = random.randint(min, max)
    print(f"随机等待{random_number}秒")
    sleep(random_number)

# 滚动到底部
def scroll_to_bottom(driver, scrollable_element):
    # 滚动到底部
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_element)
    
    # 等待页面加载
    _sleep(10, 20)
    
    # 更新当前滚动位置
    current_scroll_top = driver.execute_script("return arguments[0].scrollTop;", scrollable_element)

    # 获取最大滚动位置
    max_scroll_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_element)

    # 获取元素的高度
    element_client_height = driver.execute_script("return arguments[0].clientHeight;", scrollable_element)
    
    # 判断是否滚动到底部
    return current_scroll_top + element_client_height >= max_scroll_height


def login(driver, username=None, password=None):
    if not username or not password:
        username, password = prompt_email_password()

    driver.get("https://www.tiktok.com/explore")
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
                (By.CSS_SELECTOR, "#app-header div#header-more-menu-icon")
            )
        )
        print("登录成功")
        _sleep(5, 10)
        return True
    except Exception as e:
        print("登录失败")
        return False


def login_with_cookie(driver):
    driver.get("https://www.tiktok.com/explore")

    
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "sessionid",
            "value": "35d8c9f913f58ae06c1ea764253c519f",
        }
    )
    # driver.add_cookie(
    #     {
    #         "domain": ".www.tiktok.com",
    #         "name": "tiktok_webapp_theme_source",
    #         "value": "auto",
    #     }
    # )
    driver.add_cookie(
        {"domain": ".tiktok.com", "name": "tt-target-idc", "value": "useast5"}
    )
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "tt-target-idc-sign",
            "value": "L1PzuJzCALub5oQTM8rYOoQZ16WJEM4oAc5eycVeFAeDL-tEnX5DMbK4FVl-orfNJxUM5t7LPo311j1dywDKls8yVw0IpLBGHzk1FfIsRZXEmiFXt_D-LYr_A1T-doHy3gr7cHZMonWKRMiLKNVxML-8fdnzCkU16rqaLmawVV1snlaDa8_kuYDiMXTkDIk0JL9BkNtr5Srv3fGiwTuRWvfYrexjQ7y6GChk6yKd3_tXb2bdlh3Jkc3uWsIahVeAA4QMNFQtnWsNZNpYgMSarsiE55LRG5pECVw72qLX0HcJzTj5diwWcWkXZ4Dxw5lO2cAGQNSK1QB0Xy6B1rw2fwll8QULMt2I3X3jhrr9FW81W0wZt7BAX_YwkiXo_2VsFas75Lch1rhzOMgEJS0GYpnz9tPm7F1F7u-RP8SG1zrulzK0E4VGDfgznuAkNBdaM7K1JMQxQarTPHW6gAJ6rRWE5ADoWFl8RQtZ_9QOJGvWBh3r0oOo2KRJdKK7OnqZ",
        }
    )

    key = "user_session"
    value = '{"uid":"7405946633051522091","lastUpdated":"1729825697484"}'
    driver.execute_script(f"window.sessionStorage.setItem('{key}', '{value}')")

    _sleep(2, 4)


def search(driver, keyword):
    driver.get("https://www.tiktok.com/explore")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#app-header div#header-more-menu-icon")
        )
    )

    _sleep(5, 10)

    # 输入搜索关键词
    print(f"输入关键词：{keyword}")
    form_elem = driver.find_element(By.CSS_SELECTOR, "#app-header form.search-input")
    input_elem = form_elem.find_element(By.XPATH, ".//input[@type='search']")
    input_elem.clear()
    input_elem.send_keys(keyword)

    _sleep(5, 10)

    # 提交搜索
    print("开始搜索")
    submit_button = form_elem.find_element(By.XPATH, ".//button[@type='submit']")
    submit_button.click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#search-tabs"))
    )

    _sleep(5, 10)

    # 切换到视频筛选
    print("切换到视频模式")
    video_tab = driver.find_element(By.ID, "tabs-0-tab-search_video")
    video_tab.click()

    ids_list = []
    search_results = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                ".//div[@data-e2e='search_video-item']",
            )
        )
    )

    _sleep(5, 10)

    print("筛选搜索结果")
    if len(search_results) >= 15:
        search_results = search_results[-15:]

    for result_item in search_results:
        url = result_item.find_element(By.TAG_NAME, "a").get_attribute("href")
        pattern = r"https://www\.tiktok\.com/.*?video/(.*?)$"
        match = re.search(pattern, url)

        if match:
            video_id = match.group(1)
            if any(item == video_id for item in ids_list) == False:
                ids_list.append(video_id)
                result_item.click()
                comment(driver, type=2, reply="hhh")
                break


# 判断评论中是否有关键词
def is_comment_have_keywords(text):
    for k in comment_keywords:
        if k in text:
            return True
    return False

def loop_comment_in_type2(driver, list=[], reply="lol", is_first_loop=False):
    comment_list = WebDriverWait(driver, 600).until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                ".css-ulyotp-DivCommentContentContainer",
            )
        )
    )
    if len(comment_list) == 0:
        print("当前视频暂无评论")
        return
    if len(comment_list) >= 20:
        comment_list = comment_list[-20:]

    for comment_item in comment_list:
        comment_id = comment_item.get_attribute("id")
        bol = comment_id in list
        if (bol == False):
            list.append(comment_id)
            try:
                p_elem = comment_item.find_element(
                    By.XPATH, ".//p[@data-e2e='comment-level-1']"
                )
                text = p_elem.find_element(By.TAG_NAME, "span").text
                bol = is_comment_have_keywords(text)
                if bol == True:
                    # 点击回复
                    print("点击回复")
                    reply_btn = comment_item.find_element(
                        By.XPATH, ".//span[@data-e2e='comment-reply-1']"
                    )
                    reply_btn.click()
                    _sleep(5, 10)

                    WebDriverWait(driver, 60).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CLASS_NAME,
                                "public-DraftEditorPlaceholder-inner",
                            )
                        )
                    )

                    try:
                        # 输入文本
                        print(f"输入评论内容：{reply}")
                        comment_inputs = driver.find_elements(
                            By.XPATH, ".//div[@contenteditable='true']"
                        )
                        comment_input = comment_inputs[0]
                        comment_input.send_keys(reply)
                        _sleep(5, 10)
                        # 发布回复
                        print("发布回复")
                        comment_submits = driver.find_elements(
                            By.XPATH, ".//div[@data-e2e='comment-post']"
                        )
                        comment_submit = comment_submits[0]
                        comment_submit.click()
                        _sleep(5, 10)

                    except Exception as e:
                        pass
            except Exception as e:
                pass
            
    container_elem = driver.find_element(By.XPATH, ".//div[@data-e2e='search-comment-container']")
    scroll_elem = container_elem.find_element(By.TAG_NAME, "div")
    bol = scroll_to_bottom(driver, scroll_elem)
    if bol == False:
        if is_first_loop:
            _sleep(10, 20)
        list = list[-40:]
        print("滚动加载评论")
        loop_comment_in_type2(driver, list, is_first_loop=False)


def comment(driver, type=1, reply="lol"):
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//div[@data-e2e='search-comment-container']")
        )
    )

    if type == 1:
        # 直接回复
        # 等待评论加载完成
        WebDriverWait(driver, 300).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "public-DraftEditorPlaceholder-inner")
            )
        )
        _sleep(5, 10)

        # 输入评论
        print(f"输入评论内容：{reply}")
        comment_inputs = driver.find_element(
            By.XPATH, ".//div[@contenteditable='true']"
        )
        length = len(comment_inputs)
        comment_input = comment_inputs[length - 1]
        comment_input.send_keys(reply)

        _sleep(5, 10)

        # 提交评论
        print("发布评论")
        comment_submits = driver.find_element(
            By.XPATH, ".//div[@data-e2e='comment-post']"
        )
        length = len(comment_submits)
        comment_submit = comment_submits[length - 1]
        comment_submit.click()

        _sleep(5, 10)

        # 关闭视频详情窗口
        print("关闭视频详情窗口")
        close_button = driver.find_element(
            By.XPATH, ".//button[@data-e2e='browse-close']"
        )
        close_button.click()

        _sleep(5, 10)

    elif type == 2:
        print("回复评论")
        # 回复评论
        loop_comment_in_type2(driver, list=[], reply=reply, is_first_loop=True)


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
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # is_login_success = login(driver, username, password)
        # if (is_login_success == False):
        #     return

        login_with_cookie(driver)

        for word in search_keywords:
            search(driver, word)

    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
