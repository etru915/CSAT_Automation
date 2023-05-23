# 2022-02-28
# 문의 유형만 추가 업데이트

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import logging
from multiprocessing import Pool
import pyautogui
import random


# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s' )
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\new_macro_upload.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

time_a = 10
time_b = 20
time_c = 10


def crawling_session(start_cnt):
    # 데이터 프레임 불러오기
    df = pd.read_excel('C:/Users/zeno915/Desktop/upload_list.xlsx', sheet_name='Sheet1',header=0, usecols="b:j", index_col= 'no')
    time.sleep(5)
    # logger.info(f'{start_cnt} DF 생성 완료')
    create_error_list = []

    #로컬 변수 설정 부분
    end_cnt = start_cnt + 4
    start_cnt_original = start_cnt

    # 크롬 OS 옵션 설정
    chrome_options = Options()
    chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
    driver.set_window_size(1500, 900)
    driver.implicitly_wait(15)

    def blocker_check():
        try:
            ip_blocker = driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                time.sleep(30)
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 발생')
                locate1 = "https://coupangarchive1585294533.zendesk.com/agent/admin/macros"
                driver.get(locate1)
                time.sleep(30)
                locate2 = "https://coupangarchive1585294533.zendesk.com/agent/admin/macros/new"
                driver.get(locate2)
                time.sleep(10)
                # driver.switch_to.window(driver.window_handles[0])
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 완료. ')
                blocker_check()
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 실패 후 재시도.  ')
            else:
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음1. ')
        except Exception as e:
            # logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음2.  ')
            pass


    # 신 sandbox 로그인 진행 부분
    driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
    driver.implicitly_wait(20)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input').click()
    time.sleep(random.randint(time_a, time_b))
    time.sleep(time_c)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input').send_keys("zeno915@coupang.com")
    time.sleep(random.randint(time_a, time_b))
    time.sleep(time_c)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[2]/input').click()
    time.sleep(random.randint(time_a, time_b))
    time.sleep(time_c)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div/div[2]/span/input').send_keys("jjangkyo21!!")
    time.sleep(random.randint(time_a, time_b))
    time.sleep(time_c)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[2]/input').click()  # 로그인 완료.
    time.sleep(random.randint(time_a, time_b))
    time.sleep(time_c)


    # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
    try:
        time.sleep(random.randint(time_a, time_b))
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div[2]/a').click()
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[1]/input').send_keys("coupang")
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div[1]/form/button').click()
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/section[1]/div/section/div/a').click()
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)

        driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input').send_keys("zeno915@coupang.com")
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[2]/input').click()
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div/div[2]/span/input').send_keys('jjangkyo21!!')
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[2]/input').click()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.switch_to.frame('zendesk-clean-admin')
        logger.info(f'로그인 완료')
    except:
        pass


    while start_cnt <= end_cnt:
# try 1 : HTML 파일 생성 시도
        try:  # try count --> 1
            blocker_check()
            #매크로 제목 입력
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').click()
            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(df['macro.title'][start_cnt])
            time.sleep(3)
            driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[2]/a').click()
            time.sleep(3)

# try 2 : CS | 문의유형
            try:  # try count --> 5
                if df['custom_fields_360027007312'][start_cnt] is not None:
                    # 작업 추가 클릭
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                    # CS|문의유형 항목 선택
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[1]/div/div/input').send_keys('CS | 문의유형')
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[1]/div/div/input').send_keys(Keys.ARROW_DOWN)
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[1]/div/div/input').send_keys(Keys.ENTER)

                    # CS|문의유형 항목 등록
                    driver.find_element_by_xpath(
                        '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[2]/div/input').send_keys(str(df['custom_fields_360027007312'][start_cnt]))
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[2]/div/input').send_keys(Keys.ENTER)
                    time.sleep(1)

                    # 우선순위 항목으로 커서 이동하여 제거
                    text_value = driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[1]/div/div/button/span[2]').text
                    if text_value == "우선 순위":
                        move_cousor = driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]')
                        action = ActionChains(driver).move_to_element(move_cousor)
                        action.perform()
                        time.sleep(0.5)
                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/button').click()
                    else:
                        pass

                else:
                    logger.info(f'{start_cnt} 번째 매크로 (CS|문의유형)이 비어 있습니다.')

# try 4 : 매크로 생성
                try:  # try count --> 13
                    # 저장 클릭
                    time.sleep(random.randint(1,5))
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click()
                    # 매크로 첫 화면에서 x 클릭
                    time.sleep(random.randint(1, 5))
                    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                    logger.info(f'{start_cnt} & 번째 &{df["macro.title"][start_cnt]}&--> 모든  --> 작업을 완료하고 등록에 성공하였습니다. & {start_cnt}')
                    start_cnt += 1

                except Exception as e:  # except count --> 4
                    logger.info(f'{start_cnt} 번째 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                    driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
                    driver.switch_to.frame('zendesk-clean-admin')
                    create_error_list.append(start_cnt)
                    start_cnt += 1
                    pass
            except Exception as e:  # except count --> 5
                logger.info(f'{start_cnt} 번째 --> CS|문의유형 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
                driver.switch_to.frame('zendesk-clean-admin')
                create_error_list.append(start_cnt)
                start_cnt += 1
                pass
        except Exception as e:  # except count --> 1
            logger.info(f'{start_cnt} 번째 HTML 파일 생성 완료에 실패하였습니다.  :: error = {e}')
            create_error_list.append(start_cnt)
            driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
            driver.switch_to.frame('zendesk-clean-admin')
            start_cnt += 1
            pass

    logger.info(f'{start_cnt_original} - {end_cnt} ~ {end_cnt}번째 작업을 완료하였습니다.')
    logger.info(f'{start_cnt_original} ~ {end_cnt}번 중 등록에 실패한 리스트입니다. :: create_error = {create_error_list}')
    # driver.close()


if __name__ == '__main__':
    x = 5
    # count_list = [x]
    count_list = [0, x * 1, x * 2, x * 3, x * 4, x * 5]
    pool = Pool(processes= 6)
    pool.map(crawling_session, count_list)

    # crawling_session(0)

