from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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


def crawling_session(start_cnt):
    # 데이터 프레임 불러오기
    df = pd.read_excel('C:/Users/zeno915/Desktop/upload_list.xlsx', sheet_name='Sheet1',header=0, usecols="b:o", index_col= 'no')
    time.sleep(5)
    # logger.info(f'{start_cnt} DF 생성 완료')
    create_error_list = []

    #로컬 변수 설정 부분
    end_cnt = start_cnt + 5
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
            logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음2.  ')
            pass

    # 신 sandbox 로그인 진행 부분
    driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros/new')
    driver.implicitly_wait(10)
    # login_frame = driver.find_element_by_xpath('/html/body/div[3]/iframe')
    # driver.switch_to.frame(login_frame)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input').click()
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/span/input').send_keys("zeno915@coupang.com")
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[2]/input').click()
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[1]/div[2]/div/div[2]/span/input').send_keys("jjangkyo21##")
    driver.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/form/div[2]/input').click()  # 로그인 완료.
    time.sleep(5)
    # # 구 sandbox 로그인 진행 부분
    # driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros/new')
    # driver.implicitly_wait(10)
    # login_frame = driver.find_element_by_xpath('/html/body/div[3]/iframe')
    # driver.switch_to.frame(login_frame)
    # driver.find_element_by_xpath('//*[@id="user_email"]').click()
    # driver.find_element_by_xpath('//*[@id="user_email"]').send_keys("zeno915@coupang.com")
    # driver.find_element_by_xpath('//*[@id="user_password"]').click()
    # # driver.find_element_by_xpath('//*[@id="user_password"]').send_keys("Jkh8209$#")
    # driver.find_element_by_xpath('//*[@id="user_password"]').send_keys("jjangkyo21##")
    # driver.find_element_by_xpath('//*[@id="sign-in-submit-button"]').click()  # 로그인 완료.

    # Production Zendesk 로그인 진행 부분
    '''
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
    time.sleep(3)

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
    # logger.info(f'로그인 완료')
    '''

    while start_cnt <= end_cnt:
# try 1 : HTML 파일 생성 시도
        try:  # try count --> 1
            driver.get('https://coupangarchive1585294533.zendesk.com/agent/admin/macros/new')
            blocker_check()
            time.sleep(10)
# try 2 : 댓글/ 설명 작성
            try:  # try count --> 2
                if df['comment_value_html'][start_cnt] is not None:
                    time.sleep(10)
                    driver.switch_to.frame('zendesk-clean-admin')
                    # 작업 추가 클릭
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                    # 댓글/설명 항목 선택
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[1]/div/div/input').send_keys('댓글/설명')
                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[1]/div/div/input').send_keys(Keys.ENTER)
                    # 댓글/설명 항목 입력
                    html_text1 = df['comment_value_html'][start_cnt]
                    # print(html_text1)
                    elm = driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]/p[1]')
                    time.sleep(1)
                    driver.execute_script("arguments[0].innerHTML = '" + str(html_text1) + "';", elm)
                    # logger.info(f'{start_cnt} 번째 --> 댓글/설명 --> 작업 완료')
                    time.sleep(1)
                else:
                    logger.info(f'{start_cnt} 번째 매크로 (댓글/설명)이 비어 있습니다.')

# try 3 : 매크로 이름 입력
                try:  # try count --> 3
                    if df['macro.title'][start_cnt] is not None:
                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/label[1]/input').click()
                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/label[1]/input').send_keys(df['macro.title'][start_cnt])
                        # logger.info(f'{start_cnt} 번째 매크로 이름 입력')
                    else:
                        logger.info(f'{start_cnt} 번째 매크로 이름이 비어 있습니다.')
# try 4 : 제목 설정
                    try:  # try count --> 4
                        if df['subject'][start_cnt] is not None:
                            # 작업 추가 클릭
                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                            # 제목 설정 항목 선택
                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[2]/div[1]/div/div/input').send_keys("제목 설정")
                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[2]/div[1]/div/div/input').send_keys(Keys.ENTER)
                            # 빈 칸에 제목 입력
                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[2]/div[2]/input').send_keys(df['subject'][start_cnt])
                            # logger.info(f'{start_cnt} 번째 --> 제목 설정 --> 작업 완료')
                        else:
                            logger.info(f'{start_cnt} 번째 매크로 (제목)이 비어 있습니다.')

# try 5 : CS | 문의유형
                        try:  # try count --> 5
                            if df['custom_fields_360027007312'][start_cnt] is not None:
                                # 작업 추가 클릭
                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                                # CS|문의유형 항목 선택
                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[1]/div/div/input').send_keys('CS | 문의유형')
                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[1]/div/div/input').send_keys(Keys.ARROW_DOWN)
                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[1]/div/div/input').send_keys(Keys.ENTER)

                                # CS|문의유형 항목 등록
                                driver.find_element_by_xpath(
                                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[2]/div/input').send_keys(df['custom_fields_360027007312'][start_cnt])
                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[2]/div/input').send_keys(Keys.ENTER)
                                time.sleep(1)
                                # logger.info(f'{start_cnt} 번째 --> CS|문의유형 --> 작업 완료')
                            else:
                                logger.info(f'{start_cnt} 번째 매크로 (CS|문의유형)이 비어 있습니다.')
# try 6 :우선 순위

                            try:  # try count --> 6
                                if df['priority'][start_cnt] is not None:
                                    # 작업 추가 클릭
                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                                    # 우선 순위 항목 선택
                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[1]/div/div/input').send_keys('우선 순위')
                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[1]/div/div/input').send_keys(Keys.ENTER)
                                    # 우선 순위 항목에 보통 입력
                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[2]/div/input').send_keys('보통')
                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[2]/div/input').send_keys(Keys.ENTER)
                                    time.sleep(0.5)
                                    # logger.info(f'{start_cnt} 번째 --> 우선 순위 --> 작업 완료')
                                else:
                                    logger.info(f'{start_cnt} 번째 매크로 (우선순위)가 비어 있습니다.')
# try 7 : 태그 추가
                                try:  # try count --> 7
                                    if df['current_tags'][start_cnt] is not None:
                                        # 작업 추가 클릭
                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                                        # 태그 추가 항목 선택
                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]/div[1]/div/div/input').send_keys('태그 추가')
                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]/div[1]/div/div/input').send_keys(Keys.ENTER)
                                        time.sleep(0.5)
                                        # 생성할 태그 내용 등록
                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]/div[2]/div/div/div/input').send_keys(str(df['current_tags'][start_cnt] + " "))
                                        # driver.find_element_by_xpath(
                                            # '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]/div[2]/div/div/div/input').send_keys(Keys.ENTER)
                                        time.sleep(0.5)
                                        # 태그 등록 완료를 위해 댓글/설명 부분 한번 클릭
                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]').click()
                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]').click()
                                        # logger.info(f'{start_cnt} 번째 --> 태그 추가 --> 작업 완료')
                                    else:
                                        logger.info(f'{start_cnt} 번째 매크로 (태그 추가)가 비어 있습니다.  :: error = {e}')
# try 8 : 태그 제거
                                    try:  # try count --> 8
                                        if df['remove_tags'][start_cnt] is not None:
                                            time.sleep(1)
                                            # 작업 추가 클릭
                                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                                            # 태그 제거 항목 선택
                                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[1]/div/div/input').send_keys('태그 제거')
                                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[1]/div/div/input').send_keys(Keys.ENTER)
                                            time.sleep(0.5)
                                            # 삭제할 태그 내용 등록
                                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[2]/div/div/div/input').send_keys(str(df['remove_tags'][start_cnt] + " "))
                                            time.sleep(0.5)
                                            # 태그 등록 완료를 위해 댓글/설명 부분 한번 클릭
                                            # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]').click()
                                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]').click()
                                            # logger.info(f'{start_cnt} 번째 --> 태그 제거 --> 작업 완료')
                                        else:
                                            logger.info(f'{start_cnt} 번째 매크로 (태그 제거)가 비어 있습니다.')
# try 9 : 담당자
                                        try:  # try count --> 9
                                            if df['assignee_id'][start_cnt] is not None:
                                                # 작업 추가 클릭
                                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                                                # 담당자 선택
                                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[1]/div/div/input').send_keys('담당자')
                                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[1]/div/div/input').send_keys(Keys.ENTER)
                                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[2]/div/input').send_keys('(현재 사용자)')
                                                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[2]/div/input').send_keys(Keys.ENTER)
                                                # logger.info(f'{start_cnt} 번째 --> 담당자 --> 작업 완료')
                                            else:
                                                logger.info(f'{start_cnt} 번째 매크로 (담당자)가 비어 있습니다.')
# try 10 : 댓글모드
                                            try:  # try count --> 10
                                                if df['comment_mode_is_public'][start_cnt] is not None:
                                                    # 작업 추가 클릭
                                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                                                    # 댓글 모드 선택
                                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[1]/div/div/input').send_keys('댓글 모드')
                                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[1]/div/div/input').send_keys(Keys.ENTER)
                                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[2]/div/input').send_keys('비공개')
                                                    driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[2]/div/input').send_keys(Keys.ENTER)
                                                    time.sleep(0.5)
                                                    # logger.info(f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료')
                                                else:
                                                    logger.info(f'{start_cnt} 번째 매크로 (댓글모드)가 비어 있습니다.')

# try 11 : CS | SLA 유형
                                                try: # try count --> 11
                                                    # pass
                                                    if df['comment_mode_is_public'][start_cnt] is not None:
                                                        # 작업 추가 클릭
                                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                                                        # 댓글 모드 선택
                                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[1]/div/div/input').send_keys('CS | SLA 유형')
                                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[1]/div/div/input').send_keys(Keys.ENTER)
                                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[2]/div/input').send_keys(df['custom_fields_900007122446'][start_cnt])
                                                        driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[2]/div/input').send_keys(Keys.ENTER)
                                                        time.sleep(0.5)
                                                        # logger.info(f'{start_cnt} 번째 --> CS | SLA 유형 --> 작업 완료')
                                                    else:
                                                        logger.info(f'{start_cnt} 번째 CS | SLA 유형가 비어 있습니다.')
# try 12 : 사용자 그룹 설정
                                                    try:
                                                        # pass
                                                        # # 사용자 그룹 설정하기
                                                        # time.sleep(2)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/button').click()
                                                        # time.sleep(0.5)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/input').send_keys('그룹의 상담원\n')
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div').click()
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('A_control-CREF')
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('B_Test-ABR')
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('C_Test-AD')
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                                                        # time.sleep(1)
                                                        # driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
# try 13 : 매크로 생성
                                                        try:  # try count --> 13
                                                            time.sleep(random.randint(1,5))
                                                            driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click()
                                                            logger.info(f'{start_cnt} & 번째 --> 모든  --> 작업을 완료하고 등록에 성공하였습니다. & {start_cnt}')
                                                            start_cnt += 1
                                                            # pyautogui.write(str(start_cnt) + ' Working end ---\n', interval=0.01)

                                                        except Exception as e:  # except count --> 13
                                                            logger.info(f'{start_cnt} 번째 --> 모든  --> 작업을 중지하고 등록에 실패하였습니다.  :: error = {e}')
                                                            create_error_list.append(start_cnt)
                                                            pass
                                                            start_cnt += 1
                                                    except Exception as e:  # except count --> 12
                                                        logger.info(f'{start_cnt} 번째 --> 사용자 그룹 설정 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                                                        create_error_list.append(start_cnt)
                                                        start_cnt += 1
                                                        pass
                                                except Exception as e:  # except count --> 11
                                                    logger.info(
                                                        f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                                                    create_error_list.append(start_cnt)
                                                    start_cnt += 1
                                                    pass
                                            except Exception as e:  # except count --> 10
                                                logger.info(f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                                                create_error_list.append(start_cnt)
                                                start_cnt += 1
                                                pass
                                        except Exception as e:  # except count --> 9
                                            logger.info(f'{start_cnt} 번째 --> 담당자 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                                            create_error_list.append(start_cnt)
                                            start_cnt += 1
                                            pass
                                    except Exception as e:  # except count --> 8
                                        logger.info(f'{start_cnt} 번째 --> 태그 제거 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                                        create_error_list.append(start_cnt)
                                        start_cnt += 1
                                        pass
                                except Exception as e:  # except count --> 7
                                    logger.info(f'{start_cnt} 번째 --> 태그 추가 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                                    create_error_list.append(start_cnt)
                                    start_cnt += 1
                                    pass
                            except Exception as e:  # except count --> 6
                                logger.info(f'{start_cnt} 번째 --> 우선 순위 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                                create_error_list.append(start_cnt)
                                start_cnt += 1
                                pass
                        except Exception as e:  # except count --> 5
                            logger.info(f'{start_cnt} 번째 --> CS|문의유형 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                            create_error_list.append(start_cnt)
                            start_cnt += 1
                            pass
                    except Exception as e:  # except count --> 4
                        logger.info(f'{start_cnt} 번째 --> 제목 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                        create_error_list.append(start_cnt)
                        start_cnt += 1
                        pass
                except Exception as e:  # except count --> 3
                    logger.info(f'{start_cnt} 번째 매크로 이름 입력에 실패하였습니다. :: error = {e}')
                    create_error_list.append(start_cnt)
                    start_cnt += 1
                    pass
            except Exception as e:  # except count --> 2
                logger.info(f'{start_cnt} 번째 --> 댓글/설명 --> 작업 완료에 실패하였습니다.  :: error = {e}')
                create_error_list.append(start_cnt)
                start_cnt += 1
                pass
        except Exception as e:  # except count --> 1
            logger.info(f'{start_cnt} 번째 HTML 파일 생성 완료에 실패하였습니다.  :: error = {e}')
            create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    logger.info(f'{start_cnt_original} - {end_cnt} ~ {end_cnt}번째 작업을 완료하였습니다.')
    logger.info(f'{start_cnt_original} ~ {end_cnt}번 중 등록에 실패한 리스트입니다. :: create_error = {create_error_list}')
    # driver.close()


if __name__ == '__main__':
    x = 0
    count_list = [x]
    # count_list = [0, x * 1, x * 2, x * 3]
    pool = Pool(processes= 1)
    pool.map(crawling_session, count_list)

    # crawling_session(0)

