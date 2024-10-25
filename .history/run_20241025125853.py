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


# username = 'user7399076925301'
# password = '@K4axNj6w@qo'

username = 'user5302058888804'
password = '@K4aEsi@D5wZ'


def kill_chrome_processes():
    processes = subprocess.check_output(['ps', 'aux']).decode()
    for line in processes.split('\n'):
        if 'chrome' in line or 'chromedriver' in line:
            pid = int(line.split()[1])
            print(f'Killing process {pid}')
            os.kill(pid, signal.SIGKILL)

def __prompt_email_password():
    u = input('账号: ')
    p = getpass.getpass(prompt='密码: ')
    return (u, p)


def login(driver, username=None, password=None):
    if not username or not password:
        username, password = __prompt_email_password()

    driver.get('https://www.tiktok.com/explore')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'header-login-button')))

    login_button = driver.find_element(By.ID, 'header-login-button')
    login_button.click()

    title_elem = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'login-modal-title'))
    )

    next_sibling = title_elem.find_element(By.XPATH, './following-sibling::*[1]')

    button_elems = next_sibling.find_elements(By.XPATH, './child::div')
    button_elems[1].click()

    sleep(2)

    form_elem = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#loginContainer form'))
    )
    a_elem = form_elem.find_element(By.TAG_NAME, 'a')
    a_elem.click()
    sleep(2)

    form_elem = driver.find_element(By.CSS_SELECTOR, '#loginContainer form')
    username_input = form_elem.find_element(By.XPATH, ".//input[@name='username']")
    username_input.send_keys(username)

    password_input = form_elem.find_element(By.XPATH, ".//input[@type='password']")
    password_input.send_keys(password)

    sleep(2)

    submit_button = form_elem.find_element(By.XPATH, ".//button[@type='submit']")
    submit_button.click()

    try:
        print('登录验证中...')
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app-header div#header-more-menu-icon'))
        )
        print('登录成功')
        sleep(5)
        return True
    except Exception as e:
        print('登录失败')
        return False


def login_with_cookie(driver):
    driver.get('https://www.tiktok.com/explore')
    driver.add_cookie({'domain': '.tiktok.com', 'name': 'uid_tt', 'value': 'e57d319f84a4cd7f01637c712ba56b8fb369863226f7f3b23cedd152d74164f1'})
    driver.add_cookie({'domain': '.tiktok.com', 'name': 'uid_tt_ss', 'value': 'e57d319f84a4cd7f01637c712ba56b8fb369863226f7f3b23cedd152d74164f1'})
    driver.add_cookie({'domain': '.tiktok.com', 'name': 'tt-target-idc', 'value': 'useast5'})
    driver.add_cookie({'domain': '.tiktok.com', 'name': 'tt-target-idc-sign', 'value': 'L1PzuJzCALub5oQTM8rYOoQZ16WJEM4oAc5eycVeFAeDL-tEnX5DMbK4FVl-orfNJxUM5t7LPo311j1dywDKls8yVw0IpLBGHzk1FfIsRZXEmiFXt_D-LYr_A1T-doHy3gr7cHZMonWKRMiLKNVxML-8fdnzCkU16rqaLmawVV1snlaDa8_kuYDiMXTkDIk0JL9BkNtr5Srv3fGiwTuRWvfYrexjQ7y6GChk6yKd3_tXb2bdlh3Jkc3uWsIahVeAA4QMNFQtnWsNZNpYgMSarsiE55LRG5pECVw72qLX0HcJzTj5diwWcWkXZ4Dxw5lO2cAGQNSK1QB0Xy6B1rw2fwll8QULMt2I3X3jhrr9FW81W0wZt7BAX_YwkiXo_2VsFas75Lch1rhzOMgEJS0GYpnz9tPm7F1F7u-RP8SG1zrulzK0E4VGDfgznuAkNBdaM7K1JMQxQarTPHW6gAJ6rRWE5ADoWFl8RQtZ_9QOJGvWBh3r0oOo2KRJdKK7OnqZ'})

def comment(driver, element):
    element.click()

    comment_input = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, ".//div[@data-e2e='comment-text']"))
    )
    comment_input.send_keys('hhh')

    sleep(2)

    comment_submit = driver.find_element(By.XPATH, ".//div[@data-e2e='comment-post']")
    comment_submit.click()

    sleep(5)

    close_button = driver.find_element(By.XPATH, ".//button[@data-e2e='browse-close']")
    close_button.click()

    sleep(5)


def search(driver, keyword):
    driver.get('https://www.tiktok.com/explore')
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#app-header div#header-more-menu-icon'))
    )

    form_elem = driver.find_element(By.CSS_SELECTOR, '#app-header form.search-input')
    input_elem = form_elem.find_element(By.XPATH, ".//input[@type='search']")
    input_elem.clear()
    input_elem.send_keys(keyword)

    sleep(2)

    submit_button = form_elem.find_element(By.XPATH, ".//button[@type='submit']")
    submit_button.click()

    tab_wrapper = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#search-tabs'))
    )
    tab_items = tab_wrapper.find_elements(By.CSS_SELECTOR, 'div.tab-item')
    tab_items[2].click()

    ids_list = []
    search_results = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                ".//div[@data-e2e='search_video-item']",
            )
        )
    )
    if len(search_results) >= 15:
        search_results = search_results[-15:]

    for result_item in search_results:
        url = result_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        pattern = r"https://www\.tiktok\.com/.*?video/(.*?)$"
        match = re.search(pattern, url)

        if match:
            video_id = match.group(1)
            if any(item == video_id for item in ids_list) == False:
                print(video_id)
                ids_list.append(video_id)
                comment(driver, result_item)
                break




def main():
    kill_chrome_processes()

    try:
        # 配置Chrome选项
        chrome_options = Options()
        # 启动无痕模式
        chrome_options.add_argument('--incognito')
        # 设置代理服务器信息
        # proxy_server = 'http://127.0.0.1:7890'
        # chrome_options.add_argument(f'--proxy-server={proxy_server}')
        # 设置ChromeDriver的路径
        service = Service(executable_path='/usr/local/bin/chromedriver')
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # is_login_success = login(driver, username, password)
        # if (is_login_success == False):
        #     return
        
        # search(driver, '熊猫')

        login_with_cookie(driver)

        sleep(600)

    finally:
        if driver is not None:
            driver.quit()


if __name__ == '__main__':
    main()
