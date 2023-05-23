# 2022-04-30
# 등록된 매크로에서 댓글/설명 부분의 내용 중 일부를 수정

#-*- coding: utf-8 -*-
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
    end_cnt = start_cnt + 29
    df = pd.read_excel('C:/Users/zeno915/Desktop/upload_list.xlsx', sheet_name='Sheet1', header=0, usecols="b:d", index_col='no')
    time.sleep(5)
    logger.info(f'DF 생성 완료')
    create_error_list = []
    chrome_options = Options()
    chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
    driver.set_window_size(1500, 900)
    driver.implicitly_wait(10)

    # Production Zendesk 로그인 진행 부분
    time.sleep(round(random.uniform(1, 10), 1))
    driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")

    driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input').send_keys("zeno915@coupang.com")
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[2]/input').click()
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div/div[2]/span/input').send_keys("jjangkyo21!@")
    time.sleep(round(random.uniform(1,8),1))
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/main/div[2]/div/div/form/div[2]/input').click()  # 로그인 완료.
    time.sleep(round(random.uniform(1,3),1))

    # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
    try:
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
        driver.get(locate)
        time.sleep(30)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div[2]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div[1]/form/div[1]/div[1]/input').send_keys("coupang")
        time.sleep(3)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div[1]/form/button').click()
        time.sleep(round(random.uniform(1, 5), 1))
        element = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/div[2]/section[1]/div/section/div/a')
        driver.execute_script("arguments[0].click();", element)
        time.sleep(20)
        driver.switch_to.window(driver.window_handles[0])
        logger.info(f'로그인 완료 및 작업 시작')

    except Exception as e:
        logger.info(f'로그인 실패하여 및 작업 재시작')
        driver.switch_to.window(driver.window_handles[0])
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
        driver.get(locate)
        driver.switch_to.frame('zendesk-clean-admin')

    def blocker_check():
        try:
            ip_blocker = driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                time.sleep(30)
                logger.info(f'{start_cnt} 번째 작업 중 IP 차단 발생')
                locate1 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
                driver.get(locate1)
                time.sleep(30)
                locate2 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/" + str(df["id"][start_cnt])
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
    locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
    driver.get(locate)
    time.sleep(10)
    driver.switch_to.frame('zendesk-clean-admin-center')
    time.sleep(5)

    while start_cnt <= end_cnt:
        try:
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').click()
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(df["macro_title"][start_cnt])
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div/div/section/div[5]/table/tbody/tr/td[2]/a').click()
            logger.info(f'{start_cnt} > 번째 작업 시작 > {df["Macro_ID"][start_cnt]}')
            time.sleep(10)

            #댓글/설명 위치 확인
            action_list = driver.find_elements_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div')
            # print("action list num: " + str(len(action_list)))
            action_list_number = 1
            text_edit_yn = 0
            for i in action_list:
                # print("  action_list_number : " + str(action_list_number) + i.text)
                action_locate = '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div['+str(action_list_number)+']/div[1]'
                action_locate_text = driver.find_element_by_xpath(action_locate).text
                # print("  action_locate : " + str(action_list_number) + action_locate_text)
                # 댓글 설명 위치 검출을 위한 조회 진행
                if action_locate_text == '댓글/설명':
                    text_line_number = 1
                    text_locate = "/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div["+str(action_list_number) + "]/div[2]/div/div[1]/div/div[1]/div[1]/p"
                    # print("  text_locate : " + text_locate)
                    # 이관 매크로 텍스트 검출
                    for j in driver.find_elements_by_xpath(text_locate):
                        # print(str(text_line_number)+ " : " + j.text)
                        finded_text1 = "■ 이관 매크로 :" in j.text or "■이관 매크로 :" in j.text or "■ 이관매크로 :" in j.text or "■ 이관 매크로:" in j.text or "◼ 이관 매크로" in j.text
                        # 이관 매크로 택스트 수정
                        if finded_text1:
                            logger.info(f'{start_cnt} > 번째 작업 > {df["Macro_ID"][start_cnt]} > {text_line_number}번째 줄에서 > {j.text} > 검출')
                            # print(str(text_line_number) + "줄에서 단어 검색")
                            finded_text2 = text_locate + "["+str(text_line_number)+"]"
                            # driver.find_element_by_xpath(finded_text2).clear()
                            driver.find_element_by_xpath(finded_text2).send_keys(Keys.END)
                            time.sleep(1)
                            driver.find_element_by_xpath(finded_text2).send_keys(Keys.LEFT_SHIFT+Keys.HOME)
                            time.sleep(1)
                            driver.find_element_by_xpath(finded_text2).send_keys(Keys.DELETE)
                            time.sleep(1)
                            driver.find_element_by_xpath(finded_text2).send_keys('■ 이관 매크로')
                            time.sleep(1)
                            driver.find_element_by_xpath(finded_text2).send_keys(Keys.END)
                            time.sleep(1)
                            driver.find_element_by_xpath(finded_text2).send_keys(Keys.LEFT_SHIFT + Keys.HOME)
                            time.sleep(1)
                            driver.find_element_by_xpath(finded_text2).send_keys(Keys.LEFT_CONTROL + "b")
                            time.sleep(1)
                            driver.find_element_by_xpath(finded_text2).click()
                            time.sleep(1)
                            # driver.execute_script("arguments[0].innerHTML = '" + str(edit_text) + "';", finded_text2)
                            # print(str(text_line_number) + "줄에서 단어 수정 완료")
                            logger.info(f'{start_cnt} > 번째 작업 > {df["Macro_ID"][start_cnt]} > {text_line_number}번째 줄에서 > {j.text} > 로 수정 완료')
                            time.sleep(1)
                            text_line_number += 1
                            text_edit_yn += 1
                        else:
                            # print("text_line_number += 1 " )
                            text_line_number += 1
                else:
                    # print("action_list_number += 1 ")
                    action_list_number += 1

            if text_edit_yn >= 1:
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click()
                time.sleep(3)
                try:
                    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                    time.sleep(3)
                    start_cnt += 1
                except Exception as e:
                    start_cnt += 1
                    time.sleep(3)
                    pass

            else:
                driver.find_element_by_xpath('/html/body/div[1]/div/header/a').click()
                try:
                    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                    start_cnt += 1
                    time.sleep(3)
                except Exception as e:
                    start_cnt += 1
                    time.sleep(3)
                    pass



        except Exception as e:
            locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
            driver.get(locate)
            time.sleep(3)
            driver.switch_to.frame('zendesk-clean-admin-center')
            time.sleep(3)
            create_error_list.append(start_cnt)
            logger.info(f'{start_cnt} > 번째 작업 > {df["Macro_ID"][start_cnt]} > 작업 실패  :: error = {e}')
            start_cnt += 1
            pass

    logger.info(f'작업을 완료하였습니다.')
    logger.info(f'등록에 실패한 리스트입니다. :: create_error = {create_error_list}')
    driver.close()


if __name__ == '__main__':
    x = 30
    # count_list = [x]
    count_list = [0, x, x*2, x*3, x*4, x*5 ]
    pool = Pool(processes=6)
    pool.map(zen_edit_access_user, count_list)
