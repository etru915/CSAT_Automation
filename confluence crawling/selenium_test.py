from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe',   chrome_options=chrome_options)

driver.get("https://kms.coupang.net/pages/viewpage.action?pageId=29747572")
driver.implicitly_wait(2)
a = driver.find_element_by_tag_name("title")
# driver.implicitly_wait(2)
# a.send_keys(Keys.CONTROL,"p")
# driver.implicitly_wait(2)
# a.send_keys(Keys.ENTER)
# driver.implicitly_wait(2)
# a.send_keys(Keys.ENTER)
# ActionChains(driver).send_keys(Keys.CONTROL, "P").perform()
# driver.implicitly_wait(2)
# ActionChains(driver).send_keys(Keys.ENTER).perform()
# driver.implicitly_wait(2)
# ActionChains(driver).send_keys(Keys.ENTER).perform()
time.sleep(5)


pyautogui.hotkey('ctrl','p')
time.sleep(5)
pyautogui.hotkey('tab')
time.sleep(0.5)
pyautogui.hotkey('tab')
time.sleep(0.5)
pyautogui.hotkey('tab')
time.sleep(0.5)
pyautogui.hotkey('tab')
time.sleep(0.5)
pyautogui.hotkey('tab')
time.sleep(3)
pyautogui.hotkey('down')
time.sleep(0.5)
pyautogui.hotkey('tab')
time.sleep(0.5)
pyautogui.hotkey('tab')
time.sleep(0.5)
pyautogui.hotkey('down')
time.sleep(3)
print(1)
pyautogui.hotkey('tab')
time.sleep(0.5)
pyautogui.hotkey('tab')
time.sleep(0.5)
time.sleep(3)
pyautogui.hotkey('enter')
time.sleep(3)
pyautogui.hotkey('enter')

driver.get('https://kms.coupang.net/pages/viewpage.action?pageId=48463900')
pyautogui.hotkey('ctrl','p')


