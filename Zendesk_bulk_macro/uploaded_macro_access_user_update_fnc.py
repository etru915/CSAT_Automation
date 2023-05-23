# 2021-08-31
# 등록된 매크로에서 사용 대상 그룹을 일괄로 변경하기
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
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
formatter = logging.Formatter('%(message)s - %(name)s - %(levelname)s -  %(asctime)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\uploaded_macro_user_update.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def zen_edit_access_user(start_cnt):
    end_cnt = start_cnt + 499
    df = pd.read_excel('C:/Users/zeno915/Desktop/upload_list.xlsx', header=0, usecols="b:d", index_col='no')
    time.sleep(5)
    logger.info(f'DF 생성 완료')
    create_error_list = []
    chrome_options = Options()
    chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
    driver.set_window_size(1500, 900)
    driver.implicitly_wait(10)



    # Production Zendesk 로그인 진행 부분
    driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21##")
    time.sleep(round(random.uniform(1,5),1))
    driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click()  # 로그인 완료.
    time.sleep(3)


    def blocker_check():
        try:
            ip_blocker = driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 발생')
                time.sleep(20)
                driver.close()
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 위해 기존 창 종료')
                try:
                    # Production Zendesk 로그인 진행 부분
                    time.sleep(20)
                    driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
                    time.sleep(10)
                    driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
                    time.sleep(3)
                    driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
                    time.sleep(3)
                    driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21##")
                    time.sleep(round(random.uniform(1, 5), 1))
                    driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click()  # 로그인 완료.
                    time.sleep(3)
                    logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 위해 새로운 창으로 로그인 완료')
                    # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
                    locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
                    driver.get(locate)
                    time.sleep(40)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.find_element_by_xpath('//*[@id="ember393"]').click()
                    time.sleep(3)
                    driver.find_element_by_xpath('//*[@id="org"]').send_keys("coupang")
                    time.sleep(3)
                    driver.find_element_by_xpath('//*[@id="ember480"]/div[1]/div[2]/div/div[1]/form/button').click()
                    time.sleep(round(random.uniform(1, 5), 1))
                    element = driver.find_element_by_xpath('//*[@id="ember559"]/div/a')
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(10)
                    driver.switch_to.window(driver.window_handles[0])
                    driver.switch_to.frame('zendesk-clean-admin')
                    logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 위패 팝업창 종료 후 iframe 전환')
                    logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 완료. ')
                except Exception as e:
                    blocker_check()
                    logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 실패 후 재시도.  ')

            else:
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음1. ')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음2.  ')

    # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
    locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
    blocker_check()
    driver.get(locate)
    time.sleep(40)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath('//*[@id="ember393"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="org"]').send_keys("coupang")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="ember480"]/div[1]/div[2]/div/div[1]/form/button').click()
    time.sleep(round(random.uniform(1,5),1))
    element = driver.find_element_by_xpath('//*[@id="ember559"]/div/a')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(10)
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.frame('zendesk-clean-admin')
    logger.info(f'로그인 완료 및 작업 시작')

    while start_cnt <= end_cnt:
        try:
            time.sleep(1)
            blocker_check()
            # 비활성 클릭
            driver.find_element_by_xpath('/html/body/div/div/section/div[3]/div[1]/div/div[2]').click()
            # logger.info(f'{start_cnt} > 작업 시작')
            title_text = df['macro.title'][start_cnt]
            #제목 입력
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(df['macro.title'][start_cnt])
            # logger.info(f'{start_cnt} > 제목입력 시작 > {title_text}')
            time.sleep(4)
            try:
                current_agent = driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[3]/a').text
            except Exception as e:
                try:
                    current_agent = driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[3]/div/a').text
                except Exception as e:
                    pass
            # logger.info(f'{start_cnt}  > current_agent :  {current_agent}')
            if current_agent == "모든 상담원":
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[3]/a').click()
                time.sleep(4)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/button').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/input').send_keys('그룹의 상담원\n')
                time.sleep(2)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('A_control-CREF')
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('B_Test-ABR')
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('C_Test-AD')
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(round(random.uniform(1,5),1))
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click() # 저장 버튼 클릭하기
                time.sleep(0.5)
                # logger.info(f'{start_cnt} > 저장버튼 클릭 완료')
                # driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click() # 제목창에 내용 지우기
                # time.sleep(0.5)
                logger.info(f'{start_cnt} & 번째 작업 완료')
                # pyautogui.write(str(start_cnt) + ' end\n', interval=0.01)
                start_cnt += 1


            elif current_agent =='A_control-CREF, B_Test-ABR, C_Test-AD':
                logger.info(f'{start_cnt} & 번째 작업 완료(기등록)')
                driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()  # 제목창에 내용 지우기
                start_cnt += 1

            else:
                logger.info(f'{start_cnt} > 모든 상담원이 아님')
                driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()  # 제목창에 내용 지우기
                start_cnt += 1
                pass

        except Exception as e:
            driver.get("https://coupangcustomersupport.zendesk.com/agent/admin/macros")
            blocker_check()
            driver.switch_to.frame('zendesk-clean-admin')
            create_error_list.append(start_cnt)
            logger.info(f'{start_cnt} 번째 작업 실패  :: error = {e}')
            start_cnt += 1
            pass

    logger.info(f'작업을 완료하였습니다.')
    logger.info(f'등록에 실패한 리스트입니다. :: create_error = {create_error_list}')
    driver.close()


if __name__ == '__main__':
    count_list = [200,800,1200,1800]
    # 0,500,1000,1500, 2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000
    pool = Pool(processes=4)
    pool.map(zen_edit_access_user, count_list)
