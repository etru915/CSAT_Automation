# 2021-08-28 중복으로 등록된 매크로의 일괄 삭제
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
import pandas as pd
import logging
from multiprocessing import Pool


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
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\macro_elimination.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def delete_macro (start_cnt) :
    end_cnt = start_cnt + 99
    work_cnt = start_cnt + 0

    # 데이터 프레임 불러오기


    try:
        # 크롬 OS 옵션 설정
        chrome_options = Options()
        chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
        driver.set_window_size(1800, 900)
        driver.implicitly_wait(15)

        # Production Zendesk 로그인 진행 부분
        driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21##")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click()  # 로그인 완료.
        time.sleep(3)

        # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
        driver.get(locate)
        time.sleep(25)
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_xpath('//*[@id="ember393"]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="org"]').send_keys("coupang")
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="ember480"]/div[1]/div[2]/div/div[1]/form/button').click()
        time.sleep(5)
        element = driver.find_element_by_xpath('//*[@id="ember559"]/div/a')
        driver.execute_script("arguments[0].click();", element)
        time.sleep(20)
        driver.switch_to.window(driver.window_handles[0])
        logger.info(f'로그인 완료')

    except Exception as e:
        logger.info(f'Macro ID :  --> 실패 : 페이지를 이동하지 못함. (work count : {work_cnt}: {e})')

    df = pd.read_excel("C:\\Users\\zeno915\\Desktop\\macro elimination list2.xlsx", index_col='no')

    for i in df['id'][start_cnt:end_cnt]:
        try:
            driver.switch_to.window(driver.window_handles[0])
            locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"+str(i)
            driver.get(locate)
            time.sleep(1)
            try:
                logger.info(f'Macro ID : {i} --> 설정 페이지 이동 (work count : {work_cnt})')
                driver.switch_to.frame('zendesk-clean-admin')
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div/button').click()  # '' 버튼 클릭
                logger.info(f'Macro ID : {i} --> 메뉴 버튼 클릭 완료 (work count : {work_cnt})')
                time.sleep(1)
                try:
                    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/ul/li[3]').click()  # 메뉴에서 삭제 버튼 클릭
                    logger.info(f'Macro ID : {i} --> 삭제 버튼 클릭 완료 (work count : {work_cnt})')
                    time.sleep(1)
                    driver.switch_to.parent_frame()
                    time.sleep(1)
                    try:
                        driver.find_element_by_xpath('/html/body/div[4]/footer/button[2]').click()  #팝업창에서 매크로 삭제 클릭
                        logger.info(f'Macro ID : {i} --> 팝업 버튼 클릭 완료 (work count : {work_cnt})')
                        time.sleep(1)
                        work_cnt += 1
                        logger.info(f'Macro ID : <{i}< --> 삭제 완료 (work count : {work_cnt})')
                        pyautogui.write(time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime()) + '  ' + str(work_cnt) + ' / ' + str(i) + ' Working end ---\n', interval=0.05)

                    except Exception as e:
                        logger.info(f'Macro ID : {i} --> 실패 : 팝업 버튼을 클릭하지 못함 (work count : {work_cnt} : {e})')
                        work_cnt += 1
                except Exception as e:
                    logger.info(f'Macro ID : {i} --> 실패 : 삭제 버튼을 클릭하지 못함 (work count : {work_cnt}: {e})')
                    work_cnt += 1
            except Exception as e:
                logger.info(f'Macro ID : {i} --> 실패 : 메뉴 버튼을 클릭하지 못함 (work count : {work_cnt}: {e})')
                work_cnt += 1
        except Exception as e:
            logger.info(f'Macro ID : {i} --> 실패 : 페이지를 이동하지 못함. (work count : {work_cnt}: {e})')
            work_cnt += 1


if __name__=='__main__':
    # count_list = [0, 10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    count_list = [0,100,200,300,400]
    pool = Pool(processes=4)
    pool.map(delete_macro, count_list)



''' 06:34:38 PM  2301  //  99king end ---
2021-0
for i in delete_error_list:
    try:
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"+str(i)
        driver.get(locate)
        time.sleep(1)
        try:
            logger.info(f'Macro ID : {i} --> 설정 페이지 이동')
            driver.switch_to.frame('zendesk-clean-admin')
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div/button').click()  # '' 버튼 클릭
            logger.info(f'Macro ID : {i} --> 메뉴 버튼 클릭 완료')
            time.sleep(1)
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div/div/div/ul/li[3]').click()  # 메뉴에서 삭제 버튼 클릭
                logger.info(f'Macro ID : {i} --> 삭제 버튼 클릭 완료')
                time.sleep(1)
                driver.switch_to.parent_frame()
                time.sleep(1)
                try:
                    driver.find_element_by_xpath('/html/body/div[4]/footer/button[2]').click()  #팝업창에서 매크로 삭제 클릭
                    logger.info(f'Macro ID : {i} --> 팝업 버튼 클릭 완료')
                    time.sleep(1)
                    logger.info(f'Macro ID : {i} --> 삭제 완료')
                except:
                    logger.info(f'Macro ID : {i} --> 실패 : 팝업 버튼을 클릭하지 못함')
            except:
                logger.info(f'Macro ID : {i} --> 실패 : 삭제 버튼을 클릭하지 못함')
        except:
            logger.info(f'Macro ID : {i} --> 실패 : 메뉴 버튼을 클릭하지 못함')
    except:
        logger.info(f'Macro ID : {i} --> 실패 : 페이지를 이동하지 못함.')
'''