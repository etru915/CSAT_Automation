# 젠데스크 매크로 페이지에 접속하여 매크로 검색 후 댓글/코멘트 부분만 파싱하여, 엑섹 파일로 저장

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
time.sleep(15)
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

macro_file_name = str(' 1001_2000 ')
macro_list = [

]

col_names = ['제목', '링크', '매크로번호', '코멘트', "비고", "추출시각"]
df = pd.DataFrame(columns=col_names)

count_comment= 1
count_list = len(macro_list)

try:
    for i in macro_list:

        print('--- 전체 ' + str(count_list) + ' 건 중 ' + str(count_comment) + ' 번째 작업시작 ---')
        pyautogui.write(time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime()) + '  ' + str(count_comment) + ' / ' + str(count_list) + ' Working Start ---\n', interval=0.05)

        if count_comment % 20 == 0:
            df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_" + str(count_comment) + "_temp_save.xlsx",
                        encoding="EUC-KR")
            print("중간 저장 완료")
            print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입

        try:
            driver.switch_to.frame('zendesk-clean-admin') # 제목 입력을 위해 프레임 전환
            time.sleep(1)
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
                    macro_comment = soup.select('#editor0 > div.zendesk-editor--rich-text-container > div.rich-text.zendesk-editor--rich-text-comment')
                    status_msg = "코멘트 HTML 파싱 완료"
                except:
                    macro_comment = 'none'
                    status_msg = "코멘트 HTML을 가져오지 못했습니다."
                    df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장_검색불가" + str(count_comment) + ".xlsx", encoding="EUC-KR")

            except:
                print("Error 발생")
                status_msg = " 제목창에 매크로 제목을 입력하지 못하였습니다."
                df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장_제목미입력 "+ str(count_comment) + ".xlsx", encoding="EUC-KR")
        except:
            print("Error 발생")
            status_msg = " 제목창을 제대로 클릭하지 못하였습니다."
            df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장_제목창클릭 "+ str(count_comment) + ".xlsx", encoding="EUC-KR")
        count_comment += 1
        title = i
        link = driver.current_url
        macro_number = i
        data = {'제목': title, '링크': link, '매크로번호': macro_number, '코멘트': macro_comment[0], "비고" : status_msg, "추출시각" : time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())}
        df = df.append(data, ignore_index=True)
        print("DF 추가 완료")
        driver.get(locate)

    df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling"+ macro_file_name + ".xlsx", encoding="EUC-KR")
    driver.close()
    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입

except:
    df.to_excel("C:/Users/zeno915/Desktop/macro/macro_crawling_임시저장 "+ str(count_comment) + ".xlsx", encoding="EUC-KR")
    driver.close()
    print("error 발생")
    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))  # 런 타임 체크를 위해 삽입





    # macro_filename = str("C:\\Users\\zeno915\\Desktop\\test\\" + str(i[-7:])+".txt")
    # with open(macro_filename, 'w',  encoding="utf-8") as file_data:
    #     file_data.write(str(macro_comment[0]))
    # print('매크로를 텍스트 파일로 저장 완료')

    # driver.switch_to.default_content()
    # print('기본 프레임으로 돌아가기')
    # time.sleep(10)
    # driver.back()
    # print('이전 페이지로 돌아가기')
    # time.sleep(5)
    # driver.switch_to.frame('zendesk-clean-admin')
    # time.sleep(5)
    # driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()

    # 뒤로가기 한 후에 제목창에 입력되어 있던 기존 제목 삭제
'''
    driver.back()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').click()  # 제목창 클릭
    driver.switch_to.frame('zendesk-clean-admin')  # 제목 입력을 위해 프레임 전환
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(Keys.CONTROL + 'a')  # 제목창 클릭
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(Keys.DELETE)
'''



