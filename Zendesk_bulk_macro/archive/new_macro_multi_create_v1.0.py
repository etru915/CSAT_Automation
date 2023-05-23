from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
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
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\new_macro_upload.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def crawling_session(start_cnt):
    #로컬 변수 설정 부분
    end_cnt = start_cnt + 5
    # 크롬 OS 옵션 설정
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=chrome_options)
    driver.set_window_size(1500, 900)

    # sandbox 로그인 진행 부분
    driver.get("https://coupangcustomersupport1573078835.zendesk.com/agent/dashboard")
    driver.implicitly_wait(10)
    login_frame = driver.find_element_by_xpath('/html/body/div[3]/iframe')
    driver.switch_to.frame(login_frame)
    driver.find_element_by_xpath('//*[@id="user_email"]').click()
    driver.find_element_by_xpath('//*[@id="user_email"]').send_keys("zeno915@coupang.com")
    driver.find_element_by_xpath('//*[@id="user_password"]').click()
    driver.find_element_by_xpath('//*[@id="user_password"]').send_keys("Jkh8209$#")
    driver.find_element_by_xpath('//*[@id="sign-in-submit-button"]').click()  # 로그인 완료.

    # 데이터 프레임 불러오기
    df = pd.read_excel('C:/Users/zeno915/Desktop/macro/API_Zen_macro_value_tester.xlsx', header=0, usecols="d,n:v")
    time.sleep(5)
    logger.info(f'{start_cnt} DF 생성 완료')

    while start_cnt <= end_cnt:
        try:
            # comment_value_html 부분을 HTML 파일로 만들고 크롬으로 열어서 Rich Text를 Clipboard에 복사
            with open('C:\\Users\\zeno915\\Desktop\\macro\\upload_html\\' + str(start_cnt) + '.html', 'w',
                      encoding='utf-8') as html_text:
                html_text.write(df['comment_value_html'][start_cnt])
            logger.info(f'{start_cnt} 번째 HTML 파일 생성 완료')
            time.sleep(3)

            locate = 'https://coupangcustomersupport1573078835.zendesk.com/agent/admin/macros/new'
            driver.switch_to.window(driver.window_handles[0])
            driver.get(locate)
            driver.switch_to.frame('zendesk-clean-admin')
            logger.info(f'{start_cnt} 번째 매크로 신규 입력 창 열기 완료')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 HTML 파일 생성 완료에 실패하였습니다.  :: error = {e}')
            pass

        #매크로 이름 입력
        try:
            if df['macro.title'][start_cnt] is not None:
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/label[1]/input')\
                    .send_keys(df['macro.title'][start_cnt])
                logger.info(f'{start_cnt} 번째 매크로 이름 입력')
            else:
                logger.info(f'{start_cnt} 번째 매크로 이름이 비어 있습니다.')

        except Exception as e:
            logger.info(f'{start_cnt} 번째 매크로 이름 입력에 실패하였습니다. :: error = {e}')
            pass

        # 작업 : 제목 설정
        try:
            if df['subject'][start_cnt] is not None:
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                                            fieldset[2]/div[2]/div/button').click()
                # 제목 설정 항목 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/\
                                                div[1]/div/div/input').send_keys("제목 설정")
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/\
                                                                div[1]/div/div/input').send_keys(Keys.ENTER)
                # 빈 칸에 제목 입력
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/\
                                                div[2]/input').send_keys(df['subject'][start_cnt])
                logger.info(f'{start_cnt} 번째 --> 제목 설정 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (제목)이 비어 있습니다.')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> 제목 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass


        #작업 : 댓글/설명
        try:
            if df['comment_value_html'][start_cnt] is not None:
                open_file = 'C:\\Users\\zeno915\\Desktop\\macro\\upload_html\\' + str(start_cnt) + '.html'
                driver.execute_script('window.open("about:blank", "_blank");')
                driver.switch_to.window(driver.window_handles[1])
                driver.get(open_file)
                time.sleep(1)
                driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL + "a")
                time.sleep(1)
                driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL + "c")
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                driver.switch_to.frame('zendesk-clean-admin')
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                                            fieldset[2]/div[2]/div/button').click()
                # 댓글/설명 항목 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                            div[2]/div[1]/div/div/input').send_keys('댓글/설명')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                            div[2]/div[1]/div/div/input').send_keys(Keys.ENTER)
                # driver.find_element_by_xpath('/html/body/div[5]/div[1]/ul/li[14]').click()
                # 댓글/설명 항목 입력
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/\
                                                div[2]/div/div[1]/div/div[1]/div[1]').send_keys(Keys.CONTROL + "v")
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.frame('zendesk-clean-admin')
                logger.info(f'{start_cnt} 번째 --> 댓글/설명 --> 작업 완료')
                time.sleep(1)
            else:
                logger.info(f'{start_cnt} 번째 매크로 (댓글/설명)이 비어 있습니다.')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> 댓글/설명 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass

        # 작업 : CS | 문의유형
        try:
            if df['custom_fields_360027007312'][start_cnt] is not None:
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                            fieldset[2]/div[2]/div/button').click()
                # CS|문의유형 항목 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                div[3]/div[1]/div/div/input').send_keys('CS | 문의유형')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                                div[3]/div[1]/div/div/input').send_keys(Keys.ARROW_DOWN)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                                div[3]/div[1]/div/div/input').send_keys(Keys.ENTER)

                # CS|문의유형 항목 등록
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[2]/div/input')\
                    .send_keys(df['custom_fields_360027007312'][start_cnt])
                driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(1)
                logger.info(f'{start_cnt} 번째 --> CS|문의유형 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (CS|문의유형)이 비어 있습니다.')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> CS|문의유형 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass

        # 작업 : 우선 순위
        try:
            if df['priority'][start_cnt] is not None:
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                                            fieldset[2]/div[2]/div/button').click()
                # 우선 순위 항목 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                            div[4]/div[1]/div/div/input').send_keys('우선 순위')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                            div[4]/div[1]/div/div/input').send_keys(Keys.ENTER)
                # 우선 순위 항목에 보통 입력
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                            div[4]/div[2]/div/input').send_keys('보통')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                            div[4]/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                logger.info(f'{start_cnt} 번째 --> 우선 순위 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (우선순위)가 비어 있습니다.')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> 우선 순위 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass

        # 작업 : 태그 추가
        try:
            if df['current_tags'][start_cnt] is not None:
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                                            fieldset[2]/div[2]/div/button').click()
                # 태그 추가 항목 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                            div[5]/div[1]/div/div/input').send_keys('태그 추가')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                            div[5]/div[1]/div/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                # 생성할 태그 내용 등록
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                     div[5]/div[2]/div/div/div/input').send_keys(str(df['current_tags'][start_cnt]+" "))
                time.sleep(0.5)
                # 태그 등록 완료를 위해 댓글/설명 부분 한번 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/\
                                            div/div/div/div[2]/div/div[1]/div/div[1]/div[1]').click()
                logger.info(f'{start_cnt} 번째 --> 태그 추가 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (태그 추가)가 비어 있습니다.  :: error = {e}')

        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> 태그 추가 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass

        # 작업 : 태그 제거
        try:
            if df['remove_tags'][start_cnt] is not None:
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                                            fieldset[2]/div[2]/div/button').click()
                # 태그 제거 항목 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                            div[6]/div[1]/div/div/input').send_keys('태그 제거')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                             div[6]/div[1]/div/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                # 삭제할 태그 내용 등록
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                            div[6]/div[2]/div/div/div/input').send_keys(str(df['remove_tags'][start_cnt]+" "))
                time.sleep(0.5)
                # 태그 등록 완료를 위해 댓글/설명 부분 한번 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]') \
                    .click()
                logger.info(f'{start_cnt} 번째 --> 태그 제거 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (태그 제거)가 비어 있습니다.')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> 태그 제거 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass


        # 작업 : 담당자
        try:
            if df['assignee_id'][start_cnt] is not None:
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                            fieldset[2]/div[2]/div/button').click()
                # 담당자 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                               div[7]/div[1]/div/div/input').send_keys('담당자')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                             div[7]/div[1]/div/div/input').send_keys(Keys.ENTER)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                            div[7]/div[2]/div/input').send_keys('(현재 사용자)')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                             div[7]/div[2]/div/input').send_keys(Keys.ENTER)
                logger.info(f'{start_cnt} 번째 --> 담당자 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (담당자)가 비어 있습니다.')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> 담당자 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass

        # 작업 : 댓글모드
        try:
            if df['comment_mode_is_public'][start_cnt] is not None:
                # 작업 추가 클릭
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/\
                                                            fieldset[2]/div[2]/div/button').click()
                # 댓글 모드 선택
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                               div[8]/div[1]/div/div/input').send_keys('댓글 모드')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                               div[8]/div[1]/div/div/input').send_keys(Keys.ENTER)
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                            div[8]/div[2]/div/input').send_keys('비공개')
                driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/\
                                                            div[8]/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                logger.info(f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (댓글모드)가 비어 있습니다.')
        except Exception as e:
            logger.info(f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            pass

        # # 완성 : 만들기
        # try:
        #     driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click()
        #     logger.info(f'{start_cnt} 번째 --> 모든  --> 작업을 완료하고 등록에 성공하였습니다.')
        # except Exception as e:
        #     logger.info(f'{start_cnt} 번째 --> 모든  --> 작업을 중지하고 등록에 실패하였습니다.  :: error = {e}')
        #     pass

        start_cnt += 1

if __name__=='__main__':
    # count_list = [0, 10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    count_list = [0, 10, 20, 30]
    pool = Pool(processes=4)
    pool = Pool()
    pool.map(crawling_session, count_list)

    # crawling_session(0)

