# Zendesk macro의 내용을 API로 호출하여 엑셀 파일에 값 저장
# macro ID를 기준으로 각각의 값을 호출하는 방식
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
import time
import pandas as pd
import logging

start_vect = time.time()

# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\API_macro_list.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# 크롬 OS 옵션 설정
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
options = webdriver.ChromeOptions()
options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
options.add_argument("User-Agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=options)


# Production Zendesk 로그인 진행 부분
driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
driver.implicitly_wait(15)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
time.sleep(3)
driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21##")
time.sleep(3)
driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click() # 로그인 완료.
time.sleep(3)

#Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
driver.get(locate)
time.sleep(10)
driver.switch_to.window(driver.window_handles[1])
driver.find_element_by_xpath('//*[@id="ember393"]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="org"]').send_keys("coupang")
time.sleep(5)
driver.find_element_by_xpath('//*[@id="ember480"]/div[1]/div[2]/div/div[1]/form/button').click()
time.sleep(5)
element = driver.find_element_by_xpath('//*[@id="ember559"]/div/a')
driver.execute_script( "arguments[0].click();", element)
driver.switch_to.window(driver.window_handles[0])
time.sleep(5)

'''
# sandbox 로그인 진행 부분
driver.get("https://coupangcustomersupport1573078835.zendesk.com/agent/dashboard")
driver.implicitly_wait(10)
login_frame = driver.find_element_by_xpath('/html/body/div[3]/iframe')
driver.switch_to.frame(login_frame)
driver.find_element_by_xpath('//*[@id="user_email"]').click()
driver.find_element_by_xpath('//*[@id="user_email"]').send_keys("zeno915@coupang.com")
driver.find_element_by_xpath('//*[@id="user_password"]').click()
driver.find_element_by_xpath('//*[@id="user_password"]').send_keys("Jkh8209$#")
driver.find_element_by_xpath('//*[@id="sign-in-submit-button"]').click()  # 로그인 완료.
'''
df_total_result = pd.DataFrame() # 빈 데이터 프레임 생성

count_page = 1 # 작업 완료 카운터
while True:
    # locate = 'https://coupangcustomersupport1573078835.zendesk.com/api/v2/macros.json?page='+str(count_page)+'&per_page=500'
    locate = 'https://support.coupang.com/api/v2/macros.json?page='+str(count_page)+'&per_page=100'
    logger.info(f'{count_page} 번째 ----> 작업 시작')
    driver.get(locate)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(count_page) + ".json", 'w',
              encoding="utf-8") as json_text:
        json_text.write(soup.get_text(" ", strip=True))
        logger.info(f'{count_page} 번째 ----> Json 파일로 저장 완료')
    time.sleep(1)
    with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(count_page) + ".txt", 'w',
              encoding="utf-8") as html_text:
        html_text.write(soup.prettify())
        logger.info(f'{count_page} 번째 ----> TXT 파일로 저장 완료')
    time.sleep(1)
    with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(count_page) + ".json", 'r',
              encoding="utf-8") as json_file:
        json_value = json.load(json_file)
        logger.info(f'{count_page} 번째 ----> Json 파일로 읽어오기 완료')

    json_next_page = pd.json_normalize(json_value)
    json_Macros = pd.json_normalize(json_value['macros'])  # 매크로 기본 정보를 데이터 프레임으로 변환
    json_actions = pd.json_normalize(json_value['macros'], record_path='actions', meta=['id'], errors='ignore')

    json_actions_drop_dup = json_actions['id'].drop_duplicates()
    df_actions = pd.DataFrame()

    for i in json_actions_drop_dup:
        data = json_actions.loc[json_actions.id == i]
        data_dict = {}
        data_dict['id'] = i
        for j, k in zip(data['field'], data['value']):
            data_dict[j] = k
        data_df = pd.DataFrame([data_dict])
        # df_actions = df_actions.append(data_df)
        df_actions = pd.concat([df_actions, data_df], ignore_index= True)

    df_page_result = pd.merge(json_Macros , df_actions, on='id',how='left')
    logger.info(f'{count_page} 번째 ----> 페이지 파싱 완료')
    df_page_result.to_excel("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_"+ str(count_page) +"df_page_result.xlsx", encoding="EUC-KR")
    logger.info(f'{count_page} 번째 ----> Excel 파일로 저장 완료')

    df_total_result = pd.concat([df_total_result, df_page_result], axis=0, join='outer',ignore_index=True)
    logger.info(f'{count_page} 번째 ----> 페이지를 통합 파일에 저장')

    if json_next_page["next_page"][0] is None:
        break
    else:
        count_page += 1
        pass

df_total_result.to_excel("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_df_total_result.xlsx", encoding="EUC-KR")
logger.info(f' 전체 페이지를 통합 파일에 저장 완료, 엑셀로 변환 완료료')
print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입
driver.close()





#
#
#
# # logger.info(f'-{1} 번째 페이지의 매크로 취합 작업 시작--------------------------')
# # pyautogui.write(time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime()) + '  ' + str(count_page) + ' / ' + str(count_list) + ' Working Start ---\n', interval=0.05)
#
# # #20건마다 임시 저장 진행
# # if count_page % 20 == 0:
# #     df.to_excel("C:/Users/zeno915/Desktop/macro/json/json "+ str(count_page) + "_temp.xlsx", encoding="EUC-KR"),
# #     print("중간 저장 완료")
# #     print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입
#
# #매크로 링크를 통해 정보 요청
# locate = 'https://coupangcustomersupport.zendesk.com/api/v2/macros.json?page='+str(1)+'&per_page=300'
# driver.get(locate)
# time.sleep(3)
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(1) + ".json", 'w',
#           encoding="utf-8") as json_text:
#     json_text.write(soup.get_text(" ", strip=True))
#
# time.sleep(1)
# with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(1) + "_html.txt", 'w',
#           encoding="utf-8") as html_text:
#     html_text.write(soup.prettify())
# time.sleep(1)
# with open("C:\\Users\\zeno915\\Desktop\\macro\\api_raw\\macro_list_" + str(1) + ".json", 'r',
#           encoding="utf-8") as json_file:
#     json_value = json.load(json_file)
#     print(" 파일 3종 저장 완료")
#
#     df1 = pd.json_normalize(json_value)  # 매크로 기본 정보를 데이터 프레임으로 변환
#     df2 = pd.json_normalize(json_value['macro'], record_path='actions')  # 매크로 내 엑션 항목을 데이터프레임으로 전환
#
#     # Action 항목에 대해 Json 형태의 텍스트를 딕셔너리 형태로 변경
#     new = {}
#     for j in range(0, len(df2)):
#         new[df2.iloc[j, 0]] = df2.iloc[j, 1]
#     df3 = pd.DataFrame(new, index=[0])  # 딕셔너리 형태로 변경된 Action 항목을 DF 형태로 전환
#     df4 = df1.join(df3)
#     df = pd.concat([df, df4], axis=0)
#     print("DF 병합 완료")
#
#     count_page += 1  # 전체 작업 중 진행 완료 작업 개수를 세는 카운터
#
#         # except Exception as e:
#         #     df.to_excel("C:/Users/zeno915/Desktop/macro/json/json " + str(count_page) + "_temp.xlsx",
#         #                 encoding="EUC-KR")
#         #     driver.close()
#         #     print("파싱 과정 과정에서 error 발생")
#         #     print(e)
#         #     print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입
#         #     count_page += 1  # 전체 작업 중 진행 완료 작업 개수를 세는 카운터
#
#     df.to_excel("C:/Users/zeno915/Desktop/macro/json/macro_list_value.xlsx", encoding="EUC-KR")
#     print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입
# #
# # except Exception as e:
# #     df.to_excel("C:/Users/zeno915/Desktop/macro/json/json "+ str(count_page) + "_temp.xlsx", encoding="EUC-KR")
# #     driver.close()
# #     print("파싱 과정이 아닌 다른 과정에서 error 발생")
# #     print(e)
# #     print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입
# #     count_page += 1  # 전체 작업 중 진행 완료 작업 개수를 세는 카운터
#
#
