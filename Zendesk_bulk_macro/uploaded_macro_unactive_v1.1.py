# 2022-03-01 중복으로 등록된 매크로의 일괄 삭제
# 샌드박스에 맞추어 매크로 bulk 비활성화
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
import pandas as pd
import logging
from multiprocessing import Pool
import random

time_a = 10
time_b = 20
time_c = 10

# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(message)s & %(asctime)s & %(name)s & %(levelname)s' )
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\macro_elimination1.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def delete_macro(start_cnt) :
    end_cnt = start_cnt + 4
    work_cnt = start_cnt + 0
    # df = pd.read_csv("C:\\Users\\zeno915\\Desktop\\macro elimination list2.csv" , index_col= 'no',encoding='utf-8')
    df = pd.read_excel("C:\\Users\\zeno915\\Desktop\\upload_list.xlsx" ,sheet_name= 'Sheet1', header=0,usecols="b:d",index_col= 'no',encoding='utf-8')

    def blocker_check():
        try:
            ip_blocker = driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 발생')
                time.sleep(30)
                locate1 = "https://coupangarchive1585294533.zendesk.com/agent/admin/macros"
                driver.get(locate1)
                time.sleep(30)
                locate2 = "https://coupangarchive1585294533.zendesk.com/agent/admin/macros"
                driver.get(locate2)
                time.sleep(10)
                # driver.switch_to.window(driver.window_handles[0])
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 해제 완료. ')
                blocker_check()
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 해제 실패 후 재시도.  ')
            else:
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 없음1. ')
        except Exception as e:
            # logger.info(f'{work_cnt} 번째 작업 중 IP 차단 없음2.  ')
            pass

    try:
        # 크롬 OS 옵션 설정
        chrome_options = Options()
        chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
        driver.set_window_size(1800, 900)
        driver.implicitly_wait(15)

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

    except:
        pass

    try:
        # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
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
    except:
        pass

    try:
        driver.switch_to.frame('zendesk-clean-admin-center')
        logger.info(f'로그인 완료')
    except:
        pass


    for i in df['macro_title'][start_cnt:end_cnt]:
        try:
            # # 비활성 버튼 클릭
            # driver.find_element_by_xpath('/html/body/div/div/section/div[3]/div[1]/div/div[2]').click()
            blocker_check()
            # 매크로 제목 입력
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(df['macro_title'][work_cnt])
            time.sleep(random.randint(2,3))
            try:
                # 첫번째 매크로 항목으로 마우스 커서 이동
                move_cousor = driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[2]/a')
                action = ActionChains(driver).move_to_element(move_cousor)
                action.perform()
                # 매크로 항목의 메뉴 버튼 클릭
                driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[5]/div/button').click()
                # 매크로 항목 메뉴 내 비활성화 버튼 클릭
                time.sleep(random.randint(1,5))
                driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[5]/div/ul/li[3]').click()
                try:
                    # 팝업 창에서 매크로 삭제 버튼 클릭
                    # driver.switch_to.parent_frame()
                    # driver.find_element_by_xpath('/html/body/div[4]/footer/button[2]').click()
                    pass
                    try:
                        # driver.switch_to.frame('zendesk-clean-admin-center')
                        # x 버튼 클릭하여 제목 삭제
                        driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                        time.sleep(3)
                        # pyautogui.write(str(work_cnt) + 'end ---\n', interval=0.05)

                        with open("C:/Users/zeno915/Desktop/macro_complete_list.txt","a", encoding="utf-8") as num:
                            num.write(str(work_cnt) +"&" + i[-7:] +"\n")

                        logger.info(f'{work_cnt} & --> 작업을 완료함 & {i})')
                        work_cnt += 1

                    except Exception as e:
                        driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
                        driver.switch_to.frame('zendesk-clean-admin-center')
                        logger.info(f'Macro ID : {i} --> 실패 : x 버튼 을 클릭하지 못함 (work count : {work_cnt} : {e})')
                        work_cnt += 1
                except Exception as e:
                    # # 삭제 실패시 빈공간 클릭
                    # driver.find_element_by_xpath('/html/body/div[6]/header/button').click()
                    # # x 버튼 클릭하여 제목 삭제
                    # driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                    driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
                    driver.switch_to.frame('zendesk-clean-admin-center')
                    logger.info(f'Macro ID : {i} &--> 실패 : 팝업 버튼을 클릭하지 못함 (work count : {work_cnt} : {e})')
                    work_cnt += 1
            except Exception as e:
                # x 버튼 클릭하여 제목 삭제
                driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
                driver.switch_to.frame('zendesk-clean-admin-center')
                # driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                # driver.switch_to.parent_frame()
                logger.info(f'Macro ID : {i} &--> 실패 : 첫번째 항목이 확인되지 않음. (work count : {work_cnt} : {e})')
                work_cnt += 1
        except Exception as e:
            driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros')
            driver.switch_to.frame('zendesk-clean-admin-center')
            logger.info(f'Macro ID : {i} &--> 실패 : iframe 변경하지 못함 (work count : {work_cnt} : {e})')
            work_cnt += 1


if __name__=='__main__':
    x = 5
    # count_list = [x]
    # pool = Pool(processes=1)
    count_list = [0, x * 1, x * 2, x * 3, x * 4, x * 5]
    pool = Pool(processes=6)
    pool.map(delete_macro, count_list)
