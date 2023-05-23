# 기존 등록된 매크로를 복제하고 사용 대상을 수정


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import logging
from multiprocessing import Pool
import pyautogui
import random
from selenium.webdriver.common.action_chains import ActionChains


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


def crawling_session(start_cnt):
    # 데이터 프레임 불러오기
    df = pd.read_excel('C:/Users/zeno915/Desktop/upload_list.xlsx', sheet_name='Sheet1',header=0, usecols="b:e", index_col= 'no')
    time.sleep(5)
    # logger.info(f'{start_cnt} DF 생성 완료')
    create_error_list = []

    #로컬 변수 설정 부분
    end_cnt = start_cnt + 200
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
                locate1 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
                driver.get(locate1)
                time.sleep(30)
                locate2 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/new"
                driver.get(locate2)
                time.sleep(10)
                # driver.switch_to.window(driver.window_handles[0])
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 완료. ')
                blocker_check()
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 실패 후 재시도.  ')
            else:
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음1. ')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음2.  ')
            pass

    # Production Zendesk 로그인 진행 부분
    time.sleep(random.randint(1,5))
    driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21##")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click()  # 로그인 완료.
    time.sleep(5)

    # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
    locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
    driver.get(locate)
    time.sleep(40)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath('//*[@id="ember393"]').click()
    time.sleep(random.randint(1,5))
    driver.find_element_by_xpath('//*[@id="org"]').send_keys("coupang")
    time.sleep(random.randint(1,5))
    driver.find_element_by_xpath('//*[@id="ember480"]/div[1]/div[2]/div/div[1]/form/button').click()
    time.sleep(random.randint(1,5))
    element = driver.find_element_by_xpath('//*[@id="ember559"]/div/a')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(10)
    driver.switch_to.window(driver.window_handles[0])
    logger.info(f'로그인 완료')

    while start_cnt <= end_cnt:
        try:
            locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/" + str(df["id"][start_cnt])
            driver.get(locate)
            time.sleep(5)
            blocker_check()
            driver.switch_to.frame('zendesk-clean-admin')
            # 사용대상 3개 모두 삭제
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/ul/li[3]/span').click()
                time.sleep(1)
            except Exception as e:
                pass
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/ul/li[2]/span').click()
                time.sleep(1)
            except Exception as e:
                pass
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/ul/li[1]/span').click()
                time.sleep(1)
            except Exception as e:
                pass
            time.sleep(3)
            # 사용대상 1개 입력
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div/div/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div/div/input').send_keys('B_TEST-ABR')
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div/div/input').send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div/div/input').send_keys(Keys.ENTER)
            time.sleep(1)
            # 원본 매크로 저장
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click()
            macro_title = str(df["title"][start_cnt])
            logger.info(f'&{start_cnt}& 번째 사용 대상 변경 및 저장을 완료하였습니다. ')
            time.sleep(5)
            start_cnt += 1

        except Exception as e:  # except count --> 1
            logger.info(f'{start_cnt} 번째 원본 저장에 실패하였습니다.  :: error = {e}')
            create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    logger.info(f'{start_cnt_original} - {end_cnt} ~ {end_cnt}번째 작업을 완료하였습니다.')
    logger.info(f'{start_cnt_original} ~ {end_cnt}번 중 등록에 실패한 리스트입니다. :: create_error = {create_error_list}')
    # driver.close()


if __name__ == '__main__':
    # x = 0
    # count_list = [x]
    # pool = Pool(processes=1)

    x = 199
    count_list = [0, x * 1, x * 2, x * 3, x * 4, x * 5]
    pool = Pool(processes= 6)

    pool.map(crawling_session, count_list)
    crawling_session(0)

