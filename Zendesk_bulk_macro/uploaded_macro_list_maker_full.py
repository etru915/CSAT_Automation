# Zendesk macro의 내용을 API로 호출하여 엑셀 파일에 값 저장
# macro ID를 기준으로 각각의 값을 호출하는 방식
# Production zendesk는 셀리니움으로 API 호출이 불가능하여 API 호출은 수동으로 진행하고 1000씩 정리된 파일을 통합하는 프로젝트
# https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page=1&per_page=1000 로 수동 호출 및 파일 저장 후 실행 필요
# 모든 데이터를 포함하는 Full 버전

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import time
import pandas as pd

start_vect = time.time()

def auto_download():
    i = 1
    time.sleep(5)
    print("작업 시작")
    while i <= 47:
        pyautogui.write('https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page='+ str(i) +'&per_page=1000\n')
        # pyautogui.write('https://coupangarchive1585294533.zendesk.com/api/v2/macros.json?page=' + str(i) + '&per_page=1000\n')
        time.sleep(20)
        pyautogui.hotkey('ctrl' , 's')
        time.sleep(10)
        pyautogui.write('macro_list_'+str(i)+'.json\n')
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(1)
        print( f'{i} 페이지 저장 완료')
        i += 1

def list_merger():
    json_total_macro = pd.DataFrame()
    list_counter = 1
    while list_counter <= 47:
        with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(list_counter ) + ".json", 'r',
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
        json_total_macro.to_excel("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_total.xlsx", encoding="EUC-KR")

if __name__ == '__main__':
    time.sleep(5)
    # auto_download()
    list_merger()

    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입



