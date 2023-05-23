# 젠데스크 매크로 페이지에 접속하여 매크로 검색 후 전체 작업항목을 파싱하여, 엑섹 파일로 저장
# TXT 파일로 각 매크로의 주요 정보를 백업

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

# 로그인 진행 부분
driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
driver.implicitly_wait(15)
time.sleep(10)
driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
time.sleep(3)
driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21##")
time.sleep(3)
driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click() # 로그인 완료.
time.sleep(3)

#매크로 탭 이동 및 Genesys 창 닫기
locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
driver.get(locate)
print("현재 URL", driver.current_url)
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
print("현재 위치",driver.get_window_position(driver.window_handles[0]))


macro_list = [ '0307042' , '0305043' , '0302018'


]


df = pd.DataFrame() # 빈 데이터 프레임 생성
count_comment = 1 # 작업 완료 카운터
count_list = len(macro_list) # 전체 작업 수량

try:
    for i in macro_list:
        print('--- 전체 ' + str(count_list) + ' 건 중 ' + str(count_comment) + ' 번째 작업시작 ---')
        pyautogui.write(time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime()) + '  ' + str(count_comment) + ' / ' + str(count_list) + ' Working Start ---\n', interval=0.05)
        # print("시간소요 1" + "training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))
        if count_comment % 20 == 0:
            df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_" + str(count_comment) + "_temp_save.xlsx",
                        encoding="EUC-KR")
            print("중간 저장 완료")
            print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입

        try:
            print("시간소요 1 " + "training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))
            driver.switch_to.frame('zendesk-clean-admin') # 제목 입력을 위해 프레임 전환
            time.sleep(1)
            print("시간소요 2 " + "training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))

        except:
            pass

        # 제목창 클릭
        try:
            print(i)
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').click()
            time.sleep(1)

            # 제목창에 메크로 제목 입력
            try:
                driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(i)
                time.sleep(3)

                # 검색된 내용 중 첫번재 항목 클릭
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div/div[1]/section/div[4]/table/tbody/tr/td[2]').click()
                    time.sleep(5)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    print('페이지 파싱 완료')
                    print(soup)
                    macro_comment = soup.select('#editor0 > div.zendesk-editor--rich-text-container > div.rich-text.zendesk-editor--rich-text-comment')
                    status_msg = "코멘트 HTML 파싱 완료"
                    print(count_comment)

                    # 매크로 내 작업 항목을 분류하여 딕셔너리 형태로 변환
                    macro_action_list = soup.select('body > div.container > div > section > form > div.z-form__body > \
                                                fieldset.z-fieldset.z-form__fieldset.z-form__fieldset--actions > div.rule-actions-fieldset > div > div > div > div')
                    action_title = []
                    action_value = []
                    action_count = 0
                    action_dict = {}
                    for i2 in macro_action_list:
                        if action_count % 2 == 0:
                            action_title.append(i2.get_text(" ", strip=True))
                        else:
                            action_value.append(i2.get_text(" ", strip=True))
                        action_dict = dict(zip(action_title, action_value))
                        action_count += 1
                    action_dict['HTML Comment'] = macro_comment[0]
                    action_dict['Page Link'] = driver.current_url
                    action_dict['Status_msg'] = status_msg
                    action_dict['Get Time'] = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())
                    print("딕셔너리 변경 완료")
                    print(action_title)
                    print(action_dict)

                    # TEXT File로 각 매크로를 백업
                    macro_subject = soup.select('body > div.container > div > header > h1')
                    with open("C:\\Users\\zeno915\\Desktop\\macro\\backup\\" + str(i) + ".txt", 'w',
                              encoding="utf-8") as file_data:
                        file_data.write("작성 시간 ::: " + time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime()))
                        file_data.write("\n" * 3 + "--------------------------------------------" + "\n" * 3)
                        file_data.write("매크로 번호 ::: " + str(i))
                        file_data.write("\n" * 3 + "--------------------------------------------" + "\n" * 3)
                        file_data.write("매크로 제목 ::: " + macro_subject[0].get_text(" ", strip=True) + "\n" * 3)
                        file_data.write("\n" * 3 + "--------------------------------------------" + "\n" * 3)
                        file_data.write("작업 리스트 ::: ")
                        file_data.write(str(action_dict))
                        file_data.write("\n" * 3 + "--------------------------------------------" + "\n" * 3)
                        file_data.write("댓글/설명 HTML ::: ")
                        file_data.write(str(macro_comment[0]))
                    print("매크로 백업 텍스트 파일 완료")

                    df = df.append(action_dict, ignore_index=True)
                    print("DF 추가 완료")
                    count_comment += 1  # 전체 작업 중 진행 완료 작업 개수를 세는 카운터

                except Exception as e:
                    print("코멘트 HTML을 가져오지 못했습니다.")
                    print(e)
                    df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장_검색불가" + str(count_comment) + ".xlsx", encoding="EUC-KR")
                    count_comment += 1  # 전체 작업 중 진행 완료 작업 개수를 세는 카운터

            except Exception as e:
                print("제목창에 매크로 제목을 입력하지 못하였습니다.")
                print(e)
                df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장_제목미입력 "+ str(count_comment) + ".xlsx", encoding="EUC-KR")
                count_comment += 1  # 전체 작업 중 진행 완료 작업 개수를 세는 카운터
        except Exception as e:
            print("제목창을 제대로 클릭하지 못하였습니다.")
            print(e)
            df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장_제목창클릭 "+ str(count_comment) + ".xlsx", encoding="EUC-KR")
            count_comment += 1  # 전체 작업 중 진행 완료 작업 개수를 세는 카운터
        driver.get(locate)

    df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling " + str(count_comment) + "건_완료.xlsx", encoding="EUC-KR")
    driver.close()
    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입

except Exception as e:
    df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장 "+ str(count_comment) + ".xlsx", encoding="EUC-KR")
    driver.close()
    print("파싱 과정이 아닌 다른 과정에서error 발생")
    print(e)
    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입
