from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
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


test_link = "https://www.tiktok.com/@ipanda365/video/7232677631337024769?is_from_webapp=1&web_id=7430629140195788296"

test_reply = "I can watch it all day!"

comment_keywords = ["panda", "cute", "Kung Fu", "kungfu"]

username = ""
password = ""

cookie_session_id = ""  # cookie中的sessionid
# cookie中的tt-target-idc-sign
cookie_sign = ""
user_session = '{"uid":"","lastUpdated":""}'  # session中的user_session


# 判断评论中是否有关键词
def is_comment_have_keywords(text):
    for k in comment_keywords:
        if k in text:
            return True
    return False


# 滚动加载评论
def scroll_comment(driver, reply_type="1", reply_text="hello", id_list=[]):
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

            if "1" in reply_type:
                try:
                    p_elem = comment_item.find_element(
                        By.XPATH, ".//span[@data-e2e='comment-level-1']"
                    )
                    text = p_elem.find_element(By.TAG_NAME, "span").text
                    # 判断评论中是否包含关键词
                    bol = is_comment_have_keywords(text)
                    if bol == True:
                        send_message(driver, id=comment_id)

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


# 评论的回复私信
def reply_comments_of_comment(driver, reply_text="hhh"):
    list = get_nodes_by_classname(driver, "div", "DivReplyContainer")

    if len(list) == 0:
        print("该评论无回复")
        return

    reply_container = list[0]
    expand_comments_of_comment(reply_container)

    comment_list = get_nodes_by_classname(
        reply_container, "div", "DivCommentItemWrapper"
    )

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
                    send_message(driver, id=comment_id, reply_text=reply_text)

            except Exception as e:
                pass


# 发送私信
def send_message(driver, id="", reply_text="hello"):
    print(f"打开用户{id}的主页")

    # 获取当前窗口句柄（这是打开的第一个窗口）
    main_window = driver.current_window_handle

    # 使用 JavaScript 打开新窗口
    driver.execute_script("window.open('');")

    # 切换到新打开的窗口
    # 首先获取所有窗口句柄
    all_windows = driver.window_handles
    # 从所有窗口中排除主窗口，得到新窗口的句柄
    new_window = [window for window in all_windows if window != main_window][0]
    # 切换到新窗口
    driver.switch_to.window(new_window)

    # 在新窗口中打开另一个网址
    is_open_success = open_page(
        driver,
        url="https://www.tiktok.com/" + id,
        keys=".//button[@data-e2e='message-button']",
    )
    if is_open_success == False:
        return

    try:
        _sleep(5, 10)

        print("点击发消息")
        message_btn = driver.find_element(
            By.XPATH, ".//button[@data-e2e='message-button']"
        )
        message_btn.click()

        _sleep(5, 10)

        print("输入私信内容")
        input_element = driver.find_element(By.XPATH, ".//div[@contenteditable='true']")
        input_element.send_keys(reply_text)

        _sleep(5, 10)

        # print("发送私信")
        # send_btn = driver.find_element(By.XPATH, ".//svg[@data-e2e='message-send']")
        # send_btn.click()

        # _sleep(5, 10)

    except Exception as e:
        print(f"打开用户{id}的主页失败")

    # 关闭新窗口
    driver.close()

    # 切换回原始窗口
    driver.switch_to.window(main_window)

    _sleep(30, 60)


# 1为评论，2为评论的评论
def message(driver, reply_type="1", reply_text="lol"):
    if "1" in reply_type or "2" in reply_type:
        if "1" in reply_type:
            # 评论列表私信
            print("模式一：评论列表私信")

        if "2" in reply_type:
            # 评论的回复私信
            print("模式二：评论的回复私信")

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
        # service = Service()
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # is_login_success = login(driver, username, password)
        # if is_login_success == False:
        #     return

        login_with_cookie(
            driver,
            cookie_session_id=cookie_session_id,
            cookie_sign=cookie_sign,
            user_session=user_session,
        )

        print("打开视频链接")
        is_open_success = open_page(
            driver, url=test_link, keys=".//div[@data-e2e='upload-icon']"
        )
        if is_open_success == False:
            return

        message(driver, reply_type="1", reply_text=test_reply)

    finally:
        print("运行结束")
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
