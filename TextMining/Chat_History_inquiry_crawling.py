from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)

"""
driver.get('https://csmessenger.coupang.net/admin/tools/find-chat?chatSessionId=20585703')
driver.implicitly_wait(2)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="username"]').send_keys("zeno915@coupang.com")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="password"]').send_keys("jjangkyo21$$")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="loginButton"]').click() # 로그인 완료.
time.sleep(5)
"""


driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
driver.implicitly_wait(2)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21$$")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click() # 로그인 완료.
time.sleep(5)

locate = "https://coupangcustomersupport.zendesk.com/agent/tickets/38383710"
driver.get(locate)
print("현재 URL", driver.current_url)
time.sleep(30)
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])
print("현재 위치",driver.get_window_position(driver.window_handles[0]))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print(soup.text)

locate = "https://coupangcustomersupport.zendesk.com/agent/tickets/38387290"
driver.get(locate)
time.sleep(10)
print("현재 URL", driver.current_url)
print("현재 위치",driver.get_window_position(driver.window_handles[0]))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print(soup.text)



'''
# Ring 로그인 시도
driver.get("https://ring.coupang.net/app/")
driver.implicitly_wait(2)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21$$")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click() # 로그인 완료.
time.sleep(5)
driver.find_element_by_xpath('//*[@id="ring"]/div[6]/div[4]/ul/li[3]/button').click()
driver.find_element_by_xpath('//*[@id="ring"]/div[6]/div[4]/ul/li[3]/ul/li[2]/button').click()
time.sleep(3)

# 채팅 이력 조회창 로그인 시도
driver.get("https://csm-excel.coupang.net/admin/tools/find-chat?width=1400&height=800")
time.sleep(5)
driver.find_element_by_xpath('//*[@id="username"]').send_keys("zeno915")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="password"]').send_keys("jjangkyo21$$")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="loginButton"]').click() # 로그인 완료.
time.sleep(5)
'''

