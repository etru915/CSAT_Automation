# 2022/04/11
# selenium을 이용하여 로그인 후 Requests 모듈을 통해 selenium의 세션값을 이용하여 Zendesk에 접속하여 API 실행
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import ssl
import pandas as pd
import json
import urllib3

chrome_options = Options()
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
driver.set_window_size(1500, 900)
driver.implicitly_wait(15)

driver.get('https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml')

s = requests.Session()
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
pause = input("로그인 완료 후 아무 키나 누르세요.")
s.headers.update(headers)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


for cookie in driver.get_cookies():
    c = {cookie['name'] : cookie['value']}
    s.cookies.update(c)

i = 1
while i <= 5:
    address = 'https://coupangcustomersupport.zendesk.com/api/v2/macros.json?include=usage_30d,usage_7d&page='+ str(i)
    res = s.get(address , verify=False)
    locate = 'C:\\Users\\zeno915\\Desktop\\macro\\api_raw_new\\macro_list_'
    with open(locate + str(i) + '.json', 'w', encoding="utf-8") as f:
        f.write(res.text)
        print(res.text)
    i += 1


json_total_macro = pd.DataFrame()
list_counter = 1
while list_counter <= 5:
    with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw_new\\macro_list_" + str(list_counter ) + ".json", 'r',
              encoding="utf-8") as json_file:
        json_value = json.load(json_file)

    # 매크로 기본 정보를 데이터 프레임으로 변환
    json_Macros = pd.json_normalize(json_value['macros'])
    # Action 정보 값을 DF로 변환
    json_actions = pd.json_normalize(json_value['macros'], record_path='actions', meta=['id'], errors='ignore')
    # ID열을 시리즈로 만들고 중복 제거
    json_actions_drop_dup = json_actions['id'].drop_duplicates()
    # 빈 데이터 프레임 df_actions 생성
    df_actions = pd.DataFrame()

    for i in json_actions_drop_dup:
        # ID 열의 시리즈 데이터를 i로 순환 시키고, i에 해당하는 필드, 벨류만 가져오기
        data = json_actions.loc[json_actions.id == i]
        data_dict = {}
        # ID를 헤더 개별 id 값을 넣어 열 생성
        data_dict['id'] = i
        # 각각의 action 필드와 밸류를 행에서 열로 변환하여 data_dict에 사전 형태로 저장
        for j, k in zip(data['field'], data['value']):
            data_dict[j] = k
        # 저장된 사전을 데이터 프레임으로 변환
        data_df = pd.DataFrame([data_dict])
        # df_actions에 각 ID별로 정리된 Action 값을 저장
        df_actions = pd.concat([df_actions, data_df], ignore_index= True)
    json_page = pd.merge(json_Macros , df_actions, on='id',how='left')
    json_total_macro =pd.concat([json_total_macro, json_page], ignore_index= True)
    print(f'{list_counter } 페이지 작업 완료')
    list_counter += 1
    json_total_macro.to_excel("C:\\Users\\zeno915\\Desktop\\macro\\api_raw_new\\macro_list_total.xlsx", encoding="EUC-KR")

