# 2022/04/11
# selenium을 이용하여 로그인 후 Requests 모듈을 통해 selenium의 세션값을 이용하여 Zendesk에 접속하여 API 실행
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import ssl

chrome_options = Options()
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
driver.set_window_size(1500, 900)
driver.implicitly_wait(15)

driver.get('https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml')

s = requests.Session()
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
pause = input("아무거나 입력")
s.headers.update(headers)
for cookie in driver.get_cookies():
    c = {cookie['name'] : cookie['value']}
    s.cookies.update(c)

# https://coupangcustomersupport.zendesk.com/api/v2/macros.json?include=usage_30d,usage_7d&page=2

res = s.get('https://coupangcustomersupport.zendesk.com/api/v2/macros/', verify=False)

print(res.text)