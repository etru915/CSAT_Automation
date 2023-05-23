# Zendesk HelpCenter의 내용을 API로 호출하여 엑셀 파일에 값 저장
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import time
import pandas as pd

start_vect = time.time()
# 크롬 OS 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)


# sandbox 로그인 진행 부분
driver.get("https://coupangcustomersupport1573078835.zendesk.com/agent/dashboard")
driver.implicitly_wait(10)
login_frame = driver.find_element_by_xpath('/html/body/div[3]/iframe')
driver.switch_to.frame(login_frame)
driver.find_element_by_xpath('//*[@id="user_email"]').click()
driver.find_element_by_xpath('//*[@id="user_email"]').send_keys("zeno915@coupang.com")
driver.find_element_by_xpath('//*[@id="user_password"]').click()
driver.find_element_by_xpath('//*[@id="user_password"]').send_keys("Jkh8209$#")
driver.find_element_by_xpath('//*[@id="sign-in-submit-button"]').click() # 로그인 완료.

locate = 'https://coupangcustomersupport1573078835.zendesk.com/api/v2/help_center/articles'
driver.get(locate)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw_helpcenter\\" + "test" + ".json", 'w',
          encoding="utf-8") as json_text:
    json_text.write(soup.get_text(" ", strip=True))

time.sleep(1)
with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw_helpcenter\\" + "test" + "_html.txt", 'w',
          encoding="utf-8") as html_text:
    html_text.write(soup.prettify())
time.sleep(1)

# with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw_helpcenter\\" + "test" + ".json", 'r',
#           encoding="utf-8") as json_file:
#     json_value = json.load(json_file)
#     print(" 파일 3종 저장 완료")