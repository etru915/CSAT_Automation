# 2023-03-06  등록된 매크로의 일괄 활성화

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import logging
from multiprocessing import Pool
import random

# 멀티 프로세스 생성 시 각 프로세스별로 시간차를 두기 위해 변수 할당
time_a = 5
time_b = 15
time_c = 5

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
## -> 아래 경로에 로그를 저장할 주소를 입력합니다.
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\macro_elimination1.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def delete_macro(start_cnt) :
    # 각 프로세스의 시작 위치와 종료 위치를 지정하는 변수
    # 예를 들어 총 1000개의 매크로를 5개의 프로세스로 작업 할 경우 --> end_cnt = start_cnt + 199 으로 설정 필요
    end_cnt = start_cnt + 127
    work_cnt = start_cnt + 0

    # 아래 위치에서 엑셀 파일을 읽어와서 작업 진행
    df = pd.read_excel("C:\\Users\\zeno915\\Desktop\\upload_list.xlsx" ,sheet_name= 'Sheet1', header=0,usecols="b:e",index_col= 'no',encoding='utf-8')
    df = df[df['Action y/n'] == 0]
    df = df.reset_index(drop=True)
    df.index.name = 'no'

    # 대량 작업 시 프로세스 별로 IP가 차단되는 경우가 발생함. IP 차단 시 첫 페이지로 돌아가서 재작업 진행
    def blocker_check():
        try:
            ip_blocker = driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 발생')
                time.sleep(30)
                locate1 = "https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros"
                driver.get(locate1)
                time.sleep(30)
                locate2 = "https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros"
                driver.get(locate2)
                time.sleep(10)
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 해제 완료. ')
                blocker_check()
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 해제 실패 후 재시도.  ')
            else:
                logger.info(f'{work_cnt} 번째 작업 중 IP 차단 없음1. ')
        except Exception as e:
            pass

    try:
        # 크롬 OS 옵션 설정
        chrome_options = Options()
        chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
        driver.set_window_size(1800, 900)
        driver.implicitly_wait(15)

        # Zendesk 매크로 페이지로 이동 및 로그인
        driver.get('https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros')
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
        driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div/div[2]/span/input').send_keys("pdmucc7712$$##")
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[2]/input').click()  # 로그인 완료.
        time.sleep(random.randint(time_a, time_b))
        time.sleep(time_c)

    except:
        blocker_check()

    try:
        driver.switch_to.frame('zendesk-clean-admin-center')
        # 비활성화버튼 클릭
        time.sleep(time_c)
        driver.find_element_by_xpath('/html/body/div/div/section/div[4]/div[1]/div/div[2]').click()
        logger.info(f'로그인 완료')
    except:
        pass


    for i in df['macro_title'][start_cnt:end_cnt]:
        try:
            # blocker_check()
            # 매크로 제목 입력
            driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(df['macro_title'][work_cnt])
            time.sleep(random.randint(2,3))
            try:
                # 첫번째 매크로 항목으로 마우스 커서 이동
                move_cousor = driver.find_element_by_xpath('/html/body/div/div/section/div[5]/table/tbody/tr/td[2]/a')
                action = ActionChains(driver).move_to_element(move_cousor)
                action.perform()
                # 매크로 항목의 메뉴 버튼 클릭
                driver.find_element_by_xpath('/html/body/div/div/section/div[5]/table/tbody/tr/td[7]/div/button').click()
                # 매크로 항목 메뉴 내 활성화 버튼 클릭
                time.sleep(random.randint(1,5))
                driver.find_element_by_xpath('/html/body/div/div/section/div[5]/table/tbody/tr/td[7]/div/ul/li[3]').click()
                try:
                    # x 버튼 클릭하여 제목 삭제
                    driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                    time.sleep(3)

                    with open("C:/Users/zeno915/Desktop/macro_complete_list.txt","a", encoding="utf-8") as num:
                        # num.write(str(work_cnt) +"&" + i[-7:] +"\n")
                        num.write(f'{i}' + "\n" )
                    logger.info(f'{work_cnt} & --> 작업을 완료함 & {i})')
                    work_cnt += 1

                except Exception as e:
                    # x 버튼 클릭하여 제목 삭제를 못한 경우
                    driver.get('https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros')
                    driver.switch_to.frame('zendesk-clean-admin-center')
                    driver.find_element_by_xpath('/html/body/div/div/section/div[4]/div[1]/div/div[2]').click()
                    logger.info(f'Macro ID : {i} --> 실패 : x 버튼 을 클릭하지 못함 (work count : {work_cnt} : {e})')
                    work_cnt += 1
            except Exception as e:
                # x 버튼 클릭하여 제목 삭제
                driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click()
                time.sleep(3)
                # 매크로 제목을 검색했으나 찾지 못한 경우
                # driver.get('https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros')
                # driver.switch_to.frame('zendesk-clean-admin-center')
                # driver.find_element_by_xpath('/html/body/div/div/section/div[4]/div[1]/div/div[2]').click()
                logger.info(f'Macro ID : {i} &--> 실패 : 첫번째 항목이 확인되지 않음. (work count : {work_cnt} : {e})')
                work_cnt += 1
        except Exception as e:
            driver.get('https://coupangcustomersupport.zendesk.com/admin/workspaces/agent-workspace/macros')
            driver.switch_to.frame('zendesk-clean-admin-center')
            driver.find_element_by_xpath('/html/body/div/div/section/div[4]/div[1]/div/div[2]').click()
            logger.info(f'Macro ID : {i} &--> 실패 : iframe 변경하지 못함 (work count : {work_cnt} : {e})')
            work_cnt += 1


if __name__=='__main__':
    # 런 타임 체크를 위해 삽입
    start_vect = time.time()
    # 싱글프로세스 테스트 창
    # x = 0
    # count_list = [x]
    # pool = Pool(processes=1)
    #멀티 프로세스 작업 창
    #멀티 프로세스 개수 설정 변수 지정
    x = 128
    count_list = [0, x * 1, x * 2, x * 3]
    pool = Pool(processes=4)
    pool.map(delete_macro, count_list)

    # 런 타임 체크를 위해 삽입
    print("training Runtime: %0.2f Minutes" % ((time.time() - start_vect) / 60))
