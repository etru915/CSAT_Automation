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
from selenium.webdriver.common.action_chains import ActionChains
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
    end_cnt = start_cnt + 12
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

    # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
    try:
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
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
        logger.info(f'로그인 완료 및 작업 시작')
    except Exception as e:
        logger.info(f'로그인 실패하여 및 작업 재시작')
        driver.switch_to.window(driver.window_handles[0])
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
        driver.get(locate)
        driver.switch_to.frame('zendesk-clean-admin')


    def retry_macro_access():
        time.sleep(30)
        print("젠데스크 주소 입력 전 : " + driver.window_handles)
        driver.switch_to.window(driver.window_handles[0])
        driver.get("https://coupangcustomersupport.zendesk.com/agent/admin/macros")
        time.sleep(30)
        print("젠데스크 주소 입력 전 : " + driver.window_handles)
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/" + str(df["macro.active"][start_cnt])
        driver.get(locate)
        logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 완료. ')

    def blocker_check():
        try:
            ip_blocker = driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                time.sleep(30)
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 발생')
                locate1 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
                driver.get(locate1)
                time.sleep(30)
                locate2 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/" + str(df["macro.active"][start_cnt])
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

    def blocker_check1():
        try:
            ip_blocker = driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 발생')
                time.sleep(30)
                driver.execute_script('window.open("https://naver.com");')
                print("새창 열은 직후 : " + driver.window_handles)
                driver.switch_to.window(driver.window_handles[0])
                driver.close()
                print("기존창 종료 직후 : " + driver.window_handles)
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 위해 기존 창 종료')
                try:
                    # Production Zendesk 로그인 진행 부분
                    time.sleep(20)
                    print("젠데스크 주소 입력 전 : " + driver.window_handles)
                    driver.switch_to.window(driver.window_handles[0])
                    driver.get("https://coupangcustomersupport.zendesk.com/agent/admin/macros")
                    time.sleep(20)
                    print("젠데스크 주소 입력 전 : " + driver.window_handles)
                    locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/" + str(df["macro.active"][start_cnt])
                    driver.get(locate)
                    driver.switch_to.window(driver.window_handles[0])
                    logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 완료. ')
                except Exception as e:
                    retry_macro_access()
                    blocker_check()
                    logger.info(f'{start_cnt} 번째 작업 중 IP 차단 해제 실패 후 재시도.  ')
            else:
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음1. ')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음2.  ')
            pass

    while start_cnt <= end_cnt:
        try:
            locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/" + str(int(df["macro.active"][start_cnt]))
            driver.get(locate)
            time.sleep(5)
            blocker_check()
            driver.switch_to.frame('zendesk-clean-admin')

            # # 댓글 모드 Error 부분 삭제하기
            # action_list = driver.find_elements_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[1]/div/div/button/span[2]')
            # j = 1
            # for i in action_list:
            #     if i.text == '댓글 모드':
            #         # print(str(j) + i.text)
            #         move_cousor = driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[' + str(j) + ']')
            #         action = ActionChains(driver).move_to_element(move_cousor)
            #         action.perform()
            #         action_locate = '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[' + str(j) + ']/button'
            #         driver.find_element_by_xpath(action_locate).click()
            #         time.sleep(1)
            #         # 작업 추가
            #         driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
            #         driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[1]/div/div/input').send_keys('댓글 모드\n')
            #         time.sleep(0.5)
            #         driver.find_element_by_xpath('/html/body/div[11]/div[1]/ul/li[2]/a').click()
            #         break
            #         # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[2]/div/input').send_keys('비공개\n')
            #     else:
            #         # print(str(j) + i.text)
            #         j += 1

            사용자 그룹 설정하기
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/button').click()
            time.sleep(0.5)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/input').send_keys('그룹의 상담원\n')
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div').click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('A_control-CREF')
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('B_Test-ABR')
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('C_Test-AD')
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)


            # time.sleep(random.choice([1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6]))
            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click() # 저장 버튼 클릭하기
            time.sleep(0.5)
            # logger.info(f'{start_cnt} > 저장버튼 클릭 완료')
            # driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click() # 제목창에 내용 지우기
            # time.sleep(0.5)
            macro_id = str(int(df["macro.active"][start_cnt]))
            logger.info(f'{start_cnt} & 번째 작업 완료 & {macro_id}')
            # pyautogui.write(str(start_cnt) + ' end\n', interval=0.01)

            # pyautogui.write(str(start_cnt) + ' end\n', interval=0.01)
            start_cnt += 1

        except Exception as e:
            driver.get("https://coupangcustomersupport.zendesk.com/agent/admin/macros")
            blocker_check()
            driver.switch_to.frame('zendesk-clean-admin')
            create_error_list.append(start_cnt)
            macro_id = str(int(df["macro.active"][start_cnt]))
            logger.info(f'{start_cnt} 번째 작업 실패 {macro_id}  :: error = {e}')
            start_cnt += 1
            pass

    logger.info(f'작업을 완료하였습니다.')
    logger.info(f'등록에 실패한 리스트입니다. :: create_error = {create_error_list}')
    driver.close()


if __name__ == '__main__':
    x = 0
    count_list = [x ]
    # count_list = [x , x + 13, x + 26 , x + 39]
    pool = Pool(processes=1)
    pool.map(zen_edit_access_user, count_list)
