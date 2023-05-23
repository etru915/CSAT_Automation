from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe',   chrome_options=chrome_options)

driver.implicitly_wait(10)
driver.get("https://coupang.okta.com/app/UserHome")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21$$")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click() # 로그인 완료.
time.sleep(1)

driver.find_element_by_xpath('//*[@id="main-content"]/div/div[2]/ul[2]/li[9]/a').click() #LMS 클릭
print("LMS 클릭")
time.sleep(1)

last_tab = driver.window_handles[-1]
driver.switch_to.window(window_name=last_tab)
print("마지막 페이지로 이동")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="form2"]/div[1]/div[2]/a').click()
time.sleep(2)
sms_code = input('SMS 코드를 입력하세요.')
driver.find_element_by_xpath('//*[@id="input4"]').send_keys(sms_code)
time.sleep(2)
driver.find_element_by_xpath('//*[@id="form2"]/div[2]/input').click()
time.sleep(2)
driver.get("https://coupang.litmos.com/admin/reports/quick/module/7258974?type=responses")
html_source = driver.page_source
soup = BeautifulSoup(html_source , 'html.parser')
print(soup.prettify()) # html을 예쁘게 출력

print("----------tr-----------")
soup.find_all('tr')
print("----------td-----------")
soup.find_all('td')


'''
driver.get("https://coupang.litmos.com/")
time.sleep(2)

driver.find_element_by_xpath('//*[@id="Username"]').send_keys("zeno_test@coupang.com")
time.sleep(2)
driver.find_element_by_xpath('//*[@id="Password"]').send_keys("jkh8209$#")
time.sleep(2)
driver.find_element_by_xpath('//*[@id="login-button"]').click()
time.sleep(5)
'''