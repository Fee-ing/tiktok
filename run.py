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


test_link = "https://www.tiktok.com/@ipanda365/video/7232677631337024769?is_from_webapp=1&web_id=7430629140195788296"

test_reply = "I can watch it all day!"

comment_keywords = ["panda", "cute", "Kung Fu", "kungfu"]

# username = "user7399076925301"
# password = "@K4axNj6w@qo"
username = "user5302058888804"
password = "@K4aEsi@D5wZ"


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
    return re.findall(r'\d+', s)

# 获取特定节点
def get_nodes_by_classname(driver, tag_name, class_name):
    all_elements = driver.find_elements(By.TAG_NAME, tag_name)
    list = []
    for element in all_elements:
        if class_name in element.get_attribute("class"):
            list.append(element)
    return list


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


def login_with_cookie(driver):
    driver.get("https://www.tiktok.com/explore")

    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "sessionid",
            "value": "9a325c234d00d7065b3a83f36b84203a",
        }
    )
    driver.add_cookie(
        {
            "domain": ".www.tiktok.com",
            "name": "tiktok_webapp_theme_source",
            "value": "auto",
        }
    )
    driver.add_cookie(
        {"domain": ".tiktok.com", "name": "tt-target-idc", "value": "useast5"}
    )
    driver.add_cookie(
        {
            "domain": ".tiktok.com",
            "name": "tt-target-idc-sign",
            "value": "H0ovO3gQmtV5LO2dMZbtwgb18cg8kLChZiaN7bO0zQ0Rq0x4_9VDoffYagLHWHWyJ_ONB7d9IPrqQiS8qjp3vnRRM2QtpyBmvg5i1C_SCWRZ2F5iUKxe5D5EO7WLLJuUC9iQ0RsmzzYO-va-tfdjYRvKJB59wid2AJRdzDf9YFDLIOpHJvGHwGMSKvpEw8ELH9gaGQLlhyqZ6uDELF8U6nSPJ6xyjd-6v4wLYwHjNWzhCFtLs9BuL4mRXk3_l8yrQhJlTF5CDRRwxD2v88zaIglRcDsNWaY1IoljCdQ2x7bvJzba6fIaKdzdp8nfls6WOnUP_sLr54BC3o2QsBTPKq5u4I5GQ-Xz2QJHpRFZmDDcCQOY2RErriYCDcQS9P3BwcAxKk7wFpdLOfOzm4vhdH-FfBgAM9YHyss1vKywX_wASm9gqb-2IVwcnbfKJZc0YgJZe7JfN4oG0BGstubDnLsMwCF1kuxagT_Hc6O5m7o3gbzW0wM7UrKgBHAnKZzj",
        }
    )

    key = "user_session"
    value = '{"uid":"7405959088293200939","lastUpdated":"1730082466605"}'
    driver.execute_script(f"window.sessionStorage.setItem('{key}', '{value}')")

    _sleep(2, 4)


# 判断评论中是否有关键词
def is_comment_have_keywords(text):
    for k in comment_keywords:
        if k in text:
            return True
    return False


# 获取点击回复后的输入框节点
def get_reply_input(driver):
    list = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                ".//div[@contenteditable='true']",
            )
        )
    )
    if len(list) > 1:
        return list[1]
    else:
        return get_reply_input(driver)


# 滚动加载评论
def scroll_comment(driver, reply_type="2", reply_text="hhh", id_list=[]):
    _sleep(30, 60)

    comment_list = get_nodes_by_classname(driver, "div", "DivCommentObjectWrapper")

    if len(comment_list) == 0:
        print("当前视频暂无评论")
        return

    last_id = None
    if len(id_list) > 0:
        last_id = id_list[len(id_list) - 1]

    if len(comment_list) >= 40:
        comment_list = comment_list[-40:]

    for comment_item in comment_list:
        # 获取评论id
        comment_id = comment_item.find_element(By.TAG_NAME, "a").get_attribute("href")
        pattern = r"https?://([^/]+)"
        comment_id = re.sub(pattern, "", comment_id).strip("/")
        if (comment_id in id_list) == False and (username in comment_id) == False:
            id_list.append(comment_id)

            if "2" in reply_type:
                try:
                    p_elem = comment_item.find_element(
                        By.XPATH, ".//span[@data-e2e='comment-level-1']"
                    )
                    text = p_elem.find_element(By.TAG_NAME, "span").text
                    # 判断评论中是否包含关键词
                    bol = is_comment_have_keywords(text)
                    if bol == True:
                        # 点击回复
                        print("点击回复")
                        reply_btn = comment_item.find_element(
                            By.XPATH, ".//span[@data-e2e='comment-reply-1']"
                        )
                        reply_btn.click()

                        _sleep(5, 10)

                        # 输入文本
                        print(f"输入评论内容：{reply_text}")
                        comment_input = comment_item.find_element(By.XPATH, ".//div[@contenteditable='true']")
                        comment_input.send_keys(reply_text)

                        _sleep(5, 10)

                        # 发布回复
                        print("发布回复")
                        comment_submit = comment_item.find_element(
                            By.XPATH, ".//div[@data-e2e='comment-post']"
                        )
                        comment_submit.click()

                        _sleep(10, 20)

                except Exception as e:
                    pass

            if "3" in reply_type:
                reply_comments_of_comment(comment_item, reply_text=reply_text)

    if last_id == id_list[len(id_list) - 1]:
        print("评论加载完毕")
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        id_list = id_list[-40:]
        scroll_comment(
            driver, reply_type=reply_type, reply_text=reply_text, id_list=id_list
        )


# 加载评论的评论
def expand_comments_of_comment(driver, num=0):
    list = get_nodes_by_classname(driver, "div", "DivViewRepliesContainer")

    if len(list) == 0:
        return
    
    elif len(list) == 1:
        print("展开评论")
        text = list[0].find_element(By.TAG_NAME, "span").text
        if any(char.isdigit() for char in text):
            # 避免打不开最后一条评论而陷入死循环
            arr = extract_digits(text)
            _num = int(arr[0])
            if _num == 1 and num == 1:
                return
            else:
                num = _num
                list[0].click()
                _sleep(20, 40)
        else:
            return
    
    elif len(list) == 2:
        print("展开评论")
        for item in list:
            text = item.find_element(By.TAG_NAME, "span").text
            if any(char.isdigit() for char in text):
                # 避免打不开最后一条评论而陷入死循环
                arr = extract_digits(text)
                _num = int(arr[0])
                if _num == 1 and num == 1:
                    return
                else:
                    num = _num
                    item.click()
                    _sleep(20, 40)
                    break

    expand_comments_of_comment(driver, num=num)


# 回复评论的评论
def reply_comments_of_comment(driver, reply_text="hhh"):
    list = get_nodes_by_classname(driver, "div", "DivReplyContainer")
    
    if len(list) == 0:
        print("该评论无回复")
        return

    reply_container = list[0]
    expand_comments_of_comment(reply_container)

    comment_list = get_nodes_by_classname(reply_container, "div", "DivCommentItemWrapper")
    
    for comment_item in comment_list:
        # 获取评论id
        comment_id = comment_item.find_element(By.TAG_NAME, "a").get_attribute("href")
        pattern = r"https?://([^/]+)"
        comment_id = re.sub(pattern, "", comment_id).strip("/")
        if (username in comment_id) == False:
            try:
                p_elem = comment_item.find_element(
                    By.XPATH, ".//span[@data-e2e='comment-level-2']"
                )
                text = p_elem.find_element(By.TAG_NAME, "span").text
                # 判断评论中是否包含关键词
                bol = is_comment_have_keywords(text)
                if bol == True:
                    # 点击回复
                    print("点击回复")
                    reply_btn = comment_item.find_element(
                        By.XPATH, ".//span[@data-e2e='comment-reply-2']"
                    )
                    reply_btn.click()

                    _sleep(5, 10)

                    # 输入文本
                    print(f"输入评论内容：{reply_text}")
                    comment_input = reply_container.find_element(By.XPATH, ".//div[@contenteditable='true']")
                    comment_input.send_keys(reply_text)

                    _sleep(5, 10)

                    # 发布回复
                    print("发布回复")
                    comment_submit = reply_container.find_element(
                        By.XPATH, ".//div[@data-e2e='comment-post']"
                    )
                    comment_submit.click()

                    _sleep(10, 20)

            except Exception as e:
                pass


def open_detail(driver, reply_link="", count=5):
    print("打开视频链接")
    driver.get(reply_link)

    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, ".//dev[@data-e2e='upload-icon']"))
        )
        return True
    except Exception as e:
        count = count - 1
        if count > 0:
            return open_detail(driver, reply_link=reply_link, count=count)
        else:
            print("打开视频链接失败")
            return False


# 1为自己发布评论，2为回复评论，3为回复评论的评论
def comment(driver, reply_type="1", reply_text="lol"):
    if "1" in reply_type:
        # 直接回复
        print("模式一：直接回复")

        _sleep(5, 10)

        # 输入评论
        print(f"输入评论内容：{reply_text}")
        comment_input = driver.find_element(By.XPATH, ".//div[@contenteditable='true']")
        comment_input.send_keys(reply_text)

        _sleep(5, 10)

        # 提交评论
        print("发布评论")
        comment_submit = driver.find_element(
            By.XPATH, ".//div[@data-e2e='comment-post']"
        )
        comment_submit.click()

        _sleep(5, 10)

    if "2" in reply_type or "3" in reply_type:
        if "2" in reply_type:
            # 回复评论
            print("模式二：回复评论")

        if "3" in reply_type:
            # 回复评论的评论
            print("模式三：回复评论的评论")

        scroll_comment(driver, reply_type=reply_type, reply_text=reply_text, id_list=[])


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

        is_login_success = login(driver, username, password)
        if is_login_success == False:
            return

        # login_with_cookie(driver)

        is_open_success = open_detail(driver, reply_link=test_link, count=5)
        if is_open_success == False:
            return

        comment(driver, reply_type="123", reply_text=test_reply)

    finally:
        print("运行结束")
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
