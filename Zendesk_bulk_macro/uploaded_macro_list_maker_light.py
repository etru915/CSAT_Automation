# Zendesk macro의 내용을 API로 호출하여 엑셀 파일에 값 저장
# macro ID를 기준으로 각각의 값을 호출하는 방식
# Production zendesk는 셀리니움으로 API 호출이 불가능하여 API 호출은 수동으로 진행하고 1000씩 정리된 파일을 통합하는 프로젝트
# https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page=1&per_page=1000 로 수동 호출 및 파일 저장 후 실행 필요
# 주요 정보만 포함하는 라이트 버전 (풀 버전은 페이지수 증가에 따른 수집 시간이 오래 소요됨)
# ID, Title, Active 여부를 확인하는 용도로 사용

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import time
import pandas as pd



def auto_download(pages_num):
    i = 1
    time.sleep(5)
    print("작업 시작")
    while i <= pages_num:
        pyautogui.write('https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page='+ str(i) +'&per_page=1000\n')
        # pyautogui.write('https://coupangarchive1585294533.zendesk.com/api/v2/macros.json?page=' + str(i) + '&per_page=1000\n')
        time.sleep(15)
        pyautogui.hotkey('ctrl' , 's')
        time.sleep(10)
        pyautogui.write('C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_'+str(i)+'.json\n')
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(2)
        print( f'{i} 페이지 저장 완료')
        i += 1


def list_merger(pages_num):
    json_total_macro = pd.DataFrame()
    list_counter = 1
    while list_counter <= pages_num:
        with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(list_counter ) + ".json", 'r',
                  encoding="utf-8") as json_file:
            json_value = json.load(json_file)
        # 매크로 기본 정보를 데이터 프레임으로 변환
        json_Macros = pd.json_normalize(json_value['macros'])
        json_Macros = json_Macros[["id","title","active","updated_at"]]
        json_total_macro =pd.concat([json_total_macro, json_Macros], ignore_index= True)
        print(f'{list_counter } 페이지 작업 완료')
        list_counter += 1
        json_total_macro.to_excel("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_total.xlsx", encoding="EUC-KR")


if __name__ == '__main__':
    start_vect = time.time()
    time.sleep(5)
    pages = 23
    # auto_download(pages)
    list_merger(pages)

    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입



