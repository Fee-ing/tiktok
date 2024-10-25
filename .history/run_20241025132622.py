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


username = 'user7399076925301'
password = '@K4axNj6w@qo'

# username = 'user5302058888804'
# password = '@K4aEsi@D5wZ'


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
    driver.add_cookie({'domain': '.tiktok.com', 'name': 'odin_tt', 'value': '88950a67260692785e7d5eb5b1349470d2f472bb7604a806b1299c9b5e41dd25ac4f74781f277431fe7070fd4759baa3c512e360ed972a79f9ee4d5e4c9e4046'})
    driver.add_cookie({'domain': '.tiktok.com', 'name': 'passport_csrf_token', 'value': 'da893805d2c6f97a65adf380ecbbb53d'})
    driver.add_cookie({'domain': '.tiktok.com', 'name': 'passport_csrf_token_default', 'value': 'da893805d2c6f97a65adf380ecbbb53d'})

    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'ak_bmsc', 'value': '039636BACC11B534862EF01478AB5BBD~000000000000000000000000000000~YAAQ1GLBF+Foh76SAQAAv5HXwRlVs8HNjwqmcp4XnlNMTtb9Gz4xPMQob6gslo4SOa1NfHHASAAZy2rZEmgpkJ9jrIFca6sNZ4rHFAfVCMVWGUGOpJSG7M66cKbBdCXAk24F/des8SZt/QRK/nTKTMh3klFUN8yaQNwt1L3n9I9Y72+0l+kGns424w59MqXWmIhQjk3hvYPgU0pT/A288KSgUa+xR2TGLg3SA+eN9Bavzr8w2ZRe9HGhZk4+cWNjkTf1iBoD6ri8iUDnz6ZEEkpyPOSFCbPJcE6B/DgC93XyyXn8zc5NGw9P8yHwK4MUutcfnmkjbPDm5CmihHOFOx9+TroXdjcCIP4CS6LC6Xl/ny5Sc10afb3a9AB+jlrfMRZtdnieygrhjaU='})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'bm_sv', 'value': '25DFC64DEB38C091FC7F1040E628AB3D~YAAQ3WLBFwbqjr6SAQAAMYwDwhn1X76PIaEokRW40sWkKGJtb80+XDTeIBj+FdjZtIRX5tML8LHEjSAGMiR2UhpucPXnhzrsQk+Y1QThJoMs1vbdptWZ6AGJzB9AAPIWK8qvVEcbfJhSwHNrrUU0VbfsBA8Q3LW3SB5sm0iUQTZpxeJ+nhGzMLSwqBiI02gIe/KcSWb/jGCiAetMN6ANSo/5d3NiKfj/SiTwgQaXklJX1j8ehcVNx6nXq2nza+pw~1'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'cmpl_token', 'value': 'AgQQAPNSF-RO0rb52574u50S_Xtq4_mSP5w3YNRyKA'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'd_ticket', 'value': '5c79f6a6c7430654565bb551f49309bb7fc8c'})
    # driver.add_cookie({'domain': '.www.tiktok.com', 'name': 'delay_guest_mode_vid', 'value': '3'})
    # driver.add_cookie({'domain': '.www.tiktok.com', 'name': 'last_login_method', 'value': 'handle'})
    # driver.add_cookie({'domain': '.www.tiktok.com', 'name': 'living_user_id', 'value': '35638188158'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'msToken', 'value': 'PM7BL1T5fRN8YnpwanwIBlVJFL1WIAepGIReqcuQABYDzy8j7VOGTY-R_V4VTzd03kHWtmTNHQeE41uCg7mNYjRVTGrsPGFvcAVQTHXwTqLZSYexMIBdqOiCRYNgpzNiJDCr_SvskzhKQt2EYrD9tJNIGQ=='})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'multi_sids', 'value': '7405946633051522091%3A35d8c9f913f58ae06c1ea764253c519f'})
    
    # driver.add_cookie({'domain': '.www.tiktok.com', 'name': 'passport_fe_beating_status', 'value': 'true'})
    # driver.add_cookie({'domain': '.www.tiktok.com', 'name': 'perf_feed_cache', 'value': '{%22expireTimestamp%22:1729990800000%2C%22itemIds%22:[%227399467813406100778%22%2C%227407120547307392286%22]}'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 's_v_web_id', 'value': 'verify_m2o5flgz_PMO4ZBI1_hMAd_4358_AX8B_V7aoe0tvVyGh'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'sessionid', 'value': '35d8c9f913f58ae06c1ea764253c519f'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'sessionid_ss', 'value': '35d8c9f913f58ae06c1ea764253c519f'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'sid_guard', 'value': '35d8c9f913f58ae06c1ea764253c519f%7C1729825688%7C15552000%7CWed%2C+23-Apr-2025+03%3A08%3A08+GMT'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'sid_tt', 'value': '35d8c9f913f58ae06c1ea764253c519f'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'sid_ucp_v1', 'value': '1.0.0-KDJlMTZhMzJhOWMyOTI1M2ViZDA4ZDMxMDIwMzJiOTdlMjdkYmU0ZmQKIgiriKWEl6fN42YQmJfsuAYYswsgDDCR65y2BjgEQOoHSAQQBBoHdXNlYXN0NSIgMzVkOGM5ZjkxM2Y1OGFlMDZjMWVhNzY0MjUzYzUxOWY'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'ssid_ucp_v1', 'value': '1.0.0-KDJlMTZhMzJhOWMyOTI1M2ViZDA4ZDMxMDIwMzJiOTdlMjdkYmU0ZmQKIgiriKWEl6fN42YQmJfsuAYYswsgDDCR65y2BjgEQOoHSAQQBBoHdXNlYXN0NSIgMzVkOGM5ZjkxM2Y1OGFlMDZjMWVhNzY0MjUzYzUxOWY'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'store-country-code', 'value': 'us'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'store-country-code-src', 'value': 'uid'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'store-idc', 'value': 'useast5'})
    # driver.add_cookie({'domain': '.www.tiktok.com', 'name': 'tiktok_webapp_theme', 'value': 'light'})
    # driver.add_cookie({'domain': '.www.tiktok.com', 'name': 'tiktok_webapp_theme_source', 'value': 'auto'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'tt-target-idc', 'value': 'useast5'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'tt-target-idc-sign', 'value': 'L1PzuJzCALub5oQTM8rYOoQZ16WJEM4oAc5eycVeFAeDL-tEnX5DMbK4FVl-orfNJxUM5t7LPo311j1dywDKls8yVw0IpLBGHzk1FfIsRZXEmiFXt_D-LYr_A1T-doHy3gr7cHZMonWKRMiLKNVxML-8fdnzCkU16rqaLmawVV1snlaDa8_kuYDiMXTkDIk0JL9BkNtr5Srv3fGiwTuRWvfYrexjQ7y6GChk6yKd3_tXb2bdlh3Jkc3uWsIahVeAA4QMNFQtnWsNZNpYgMSarsiE55LRG5pECVw72qLX0HcJzTj5diwWcWkXZ4Dxw5lO2cAGQNSK1QB0Xy6B1rw2fwll8QULMt2I3X3jhrr9FW81W0wZt7BAX_YwkiXo_2VsFas75Lch1rhzOMgEJS0GYpnz9tPm7F1F7u-RP8SG1zrulzK0E4VGDfgznuAkNBdaM7K1JMQxQarTPHW6gAJ6rRWE5ADoWFl8RQtZ_9QOJGvWBh3r0oOo2KRJdKK7OnqZ'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'tt_chain_token', 'value': 's4aB7PzAjnBkyFGqceAW/w=='})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'tt_csrf_token', 'value': '665Y6fiP-pqnD-ZIZP0i47D1PNDnf8NX6Qx4'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'ttwid', 'value': '1%7CSQooGgmwmkI4ZHjglAHKLX1i3shEoAf3PCMbXtIroHw%7C1729831831%7C295cdfcb29ce97bad010540dfecf6284d6eb68db7233b380cf82b104842f7eca'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'uid_tt', 'value': 'e57d319f84a4cd7f01637c712ba56b8fb369863226f7f3b23cedd152d74164f1'})
    # driver.add_cookie({'domain': '.tiktok.com', 'name': 'uid_tt_ss', 'value': 'e57d319f84a4cd7f01637c712ba56b8fb369863226f7f3b23cedd152d74164f1'})


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
