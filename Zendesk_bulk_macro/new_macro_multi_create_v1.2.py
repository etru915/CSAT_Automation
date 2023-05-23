# 1.1 버전을 클래스 버전으로 포팅하기
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
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s - %(asctime)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('C:\\Users\\zeno915\\Desktop\\macro\\new_macro_upload.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ZendeskEdit:
    create_error_list = []
    def __init__(self,start_cnt):
        end_cnt = start_cnt + 99
        start_cnt_original = start_cnt

        # 크롬 OS 옵션 설정
        self.chrome_options = Options()
        self.chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        self.driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=self.chrome_options)
        self.driver.set_window_size(1500, 900)
        self.driver.implicitly_wait(15)

        # sandbox 로그인 진행 부분
        '''
        driver.get('https://coupangcustomersupport1573078835.zendesk.com/agent/admin/macros/new')
        driver.implicitly_wait(10)
        login_frame = driver.find_element_by_xpath('/html/body/div[3]/iframe')
        driver.switch_to.frame(login_frame)
        driver.find_element_by_xpath('//*[@id="user_email"]').click()
        driver.find_element_by_xpath('//*[@id="user_email"]').send_keys("zeno915@coupang.com")
        driver.find_element_by_xpath('//*[@id="user_password"]').click()
        driver.find_element_by_xpath('//*[@id="user_password"]').send_keys("Jkh8209$#")
        driver.find_element_by_xpath('//*[@id="sign-in-submit-button"]').click()  # 로그인 완료.
        '''

        # Production Zendesk 로그인 진행 부분
        self.driver.get("https://coupang.okta.com/app/zendesk/exk8bcxnfe6v9XM3N2p7/sso/saml")
        time.sleep(10)
        self.driver.find_element_by_xpath('//*[@id="idp-discovery-username"]').send_keys("zeno915@coupang.com")
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="idp-discovery-submit"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="input8"]').send_keys("jjangkyo21##")
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="form6"]/div[2]/input').click()  # 로그인 완료.
        time.sleep(3)

        # Production Zendesk 매크로 탭 이동 및 Genesys 창 닫기
        locate = "https://coupangcustomersupport.zendesk.com/agent/admin/macros"
        self.driver.get(locate)
        time.sleep(40)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_xpath('//*[@id="ember393"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="org"]').send_keys("coupang")
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="ember480"]/div[1]/div[2]/div/div[1]/form/button').click()
        time.sleep(3)
        self.element = self.driver.find_element_by_xpath('//*[@id="ember559"]/div/a')
        self.driver.execute_script("arguments[0].click();", self.element)
        time.sleep(10)
        self.driver.switch_to.window(self.driver.window_handles[0])
        logger.info(f'로그인 완료')
    def blocker_check(self):
        try:
            ip_blocker = self.driver.find_element_by_xpath('/html/body/article/h1').text
            if ip_blocker == 'Your IP address is not permitted.':
                time.sleep(30)
                logger.info(f'{self.start_cnt} 번째 작업 중 IP 차단 발생')
                locate1 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/"
                self.driver.get(locate1)
                time.sleep(30)
                locate2 = "https://coupangcustomersupport.zendesk.com/agent/admin/macros/new"
                self.driver.get(locate2)
                time.sleep(10)
                # driver.switch_to.window(driver.window_handles[0])
                logger.info(f'{self.start_cnt} 번째 작업 중 IP 차단 해제 완료. ')
                self.blocker_check()
                logger.info(f'{self.start_cnt} 번째 작업 중 IP 차단 해제 실패 후 재시도.  ')
            else:
                logger.info(f'{self.start_cnt} 번째 작업 중 IP 차단 없음1. ')
        except Exception as e:
            # logger.info(f'{start_cnt} 번째 작업 중 IP 차단 없음2.  ')
            pass
    def making_df(self):
        # 데이터 프레임 불러오기
        self.df = pd.read_excel('C:/Users/zeno915/Desktop/upload_list.xlsx', header=0, usecols="a:n", index_col='no')
        time.sleep(5)
        logger.info(f'DF 생성 완료')
    def moving_site(self,start_cnt):
        try:
            self.driver.get('https://coupangcustomersupport.zendesk.com/agent/admin/macros/new')
            self.blocker_check()
        except Exception as e:  # except count --> 1
            logger.info(f'{start_cnt} 번째 HTML 파일 생성 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    def comment_update(self,start_cnt):
        try:  # try count --> 2
            if self.df['comment_value_html'][start_cnt] is not None:
                time.sleep(1)
                self.driver.switch_to.frame('zendesk-clean-admin')
                # 작업 추가 클릭
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 댓글/설명 항목 선택
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[1]/div/div/input').send_keys(
                    '댓글/설명')
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[1]/div/div/input').send_keys(
                    Keys.ENTER)
                # 댓글/설명 항목 입력
                html_text1 = self.df['comment_value_html'][start_cnt]
                # print(html_text1)
                elm = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]/p[1]')
                time.sleep(1)
                self.driver.execute_script("arguments[0].innerHTML = '" + str(html_text1) + "';", elm)
                logger.info(f'{start_cnt} 번째 --> 댓글/설명 --> 작업 완료')
                time.sleep(1)
            else:
                logger.info(f'{start_cnt} 번째 매크로 (댓글/설명)이 비어 있습니다.')
        except Exception as e:  # except count --> 2
            logger.info(f'{start_cnt} 번째 --> 댓글/설명 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
    def macro_name_update(self,start_cnt): # try 3 : 매크로 이름 입력
        try:
            if self.df['macro.title'][start_cnt] is not None:
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[1]/label[1]/input').click()
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[1]/label[1]/input').send_keys(
                    self.df['macro.title'][start_cnt])
                logger.info(f'{start_cnt} 번째 매크로 이름 입력')
            else:
                logger.info(f'{start_cnt} 번째 매크로 이름이 비어 있습니다.')
        except Exception as e:  # except count --> 3
            logger.info(f'{start_cnt} 번째 매크로 이름 입력에 실패하였습니다. :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
        pass
    def macro_subject_update(self,start_cnt):  # try 4 : 제목 설정
        try:  # try count --> 4
            if self.df['subject'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 제목 설정 항목 선택
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[2]/div[1]/div/div/input').send_keys("제목 설정")
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[2]/div[1]/div/div/input').send_keys(Keys.ENTER)
                # 빈 칸에 제목 입력
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[2]/div[2]/input').send_keys(self.df['subject'][start_cnt])
                logger.info(f'{start_cnt} 번째 --> 제목 설정 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (제목)이 비어 있습니다.')
        except Exception as e:  # except count --> 4
            logger.info(f'{start_cnt} 번째 --> 제목 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    def category_update(self,start_cnt):
        # try 5 : CS | 문의유형
        try:  # try count --> 5
            if self.df['custom_fields_360027007312'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # CS|문의유형 항목 선택
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[1]/div/div/input').send_keys('CS | 문의유형')
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[1]/div/div/input').send_keys(Keys.ARROW_DOWN)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[1]/div/div/input').send_keys(Keys.ENTER)

                # CS|문의유형 항목 등록
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[2]/div/input').send_keys(self.df['custom_fields_360027007312'][start_cnt])
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[3]/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(1)
                logger.info(f'{start_cnt} 번째 --> CS|문의유형 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (CS|문의유형)이 비어 있습니다.')
        except Exception as e:  # except count --> 5
            logger.info(f'{start_cnt} 번째 --> CS|문의유형 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
    def priority_update(self,start_cnt):
        # try 6 :우선 순위
        try:  # try count --> 6
            if self.df['priority'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 우선 순위 항목 선택
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[1]/div/div/input').send_keys('우선 순위')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[1]/div/div/input').send_keys(Keys.ENTER)
                # 우선 순위 항목에 보통 입력
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[2]/div/input').send_keys('보통')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[4]/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                logger.info(f'{start_cnt} 번째 --> 우선 순위 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (우선순위)가 비어 있습니다.')

        except Exception as e:  # except count --> 6
            logger.info(f'{start_cnt} 번째 --> 우선 순위 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    def add_tag_update(self,start_cnt):
        # try 7 : 태그 추가
        try:  # try count --> 7
            if self.df['current_tags'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 태그 추가 항목 선택
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]/div[1]/div/div/input').send_keys('태그 추가')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]/div[1]/div/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                # 생성할 태그 내용 등록
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[5]/div[2]/div/div/div/input').send_keys(str(self.df['current_tags'][start_cnt] + " "))
                time.sleep(0.5)
                # 태그 등록 완료를 위해 댓글/설명 부분 한번 클릭
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]').click()
                logger.info(f'{start_cnt} 번째 --> 태그 추가 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (태그 추가)가 비어 있습니다.  ')
        except Exception as e:  # except count --> 7
            logger.info(f'{start_cnt} 번째 --> 태그 추가 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    def remove_tag_update(self,start_cnt):
        # try 8 : 태그 제거
        try:  # try count --> 8
            if self.df['remove_tags'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 태그 제거 항목 선택
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[1]/div/div/input').send_keys('태그 제거')
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[1]/div/div/input').send_keys(Keys.ENTER)
                time.sleep(1)
                # 삭제할 태그 내용 등록
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[6]/div[2]/div/div/div/input').send_keys(str(self.df['remove_tags'][start_cnt] + " "))
                time.sleep(1)
                # 태그 등록 완료를 위해 댓글/설명 부분 한번 클릭
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]').click()
                logger.info(f'{start_cnt} 번째 --> 태그 제거 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (태그 제거)가 비어 있습니다.')
        except Exception as e:  # except count --> 8
            logger.info(f'{start_cnt} 번째 --> 태그 제거 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
    def pic_update(self,start_cnt):
        # try 9 : 담당자
        try:  # try count --> 9
            if self.df['assignee_id'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 담당자 선택
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[1]/div/div/input').send_keys(
                    '담당자')
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[1]/div/div/input').send_keys(
                    Keys.ENTER)
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[2]/div/input').send_keys(
                    '(현재 사용자)')
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[7]/div[2]/div/input').send_keys(
                    Keys.ENTER)
                logger.info(f'{start_cnt} 번째 --> 담당자 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (담당자)가 비어 있습니다.')
        except Exception as e:  # except count --> 9
            logger.info(f'{start_cnt} 번째 --> 담당자 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
    def comment_mode_update(self,start_cnt):
        # try 10 : 댓글모드
        try:  # try count --> 10
            if self.df['comment_mode_is_public'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 댓글 모드 선택
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[1]/div/div/input').send_keys('댓글 모드')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[1]/div/div/input').send_keys(Keys.ENTER)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[2]/div/input').send_keys('비공개')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[8]/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                logger.info(f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 매크로 (댓글모드)가 비어 있습니다.')
        except Exception as e:  # except count --> 10
            logger.info(f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    def sla_update(self,start_cnt):
        # try 11 : CS | SLA 유형
        try:  # try count --> 11
            if self.df['comment_mode_is_public'][start_cnt] is not None:
                # 작업 추가 클릭
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/button').click()
                # 댓글 모드 선택
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[1]/div/div/input').send_keys('CS | SLA 유형')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[1]/div/div/input').send_keys(Keys.ENTER)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[2]/div/input').send_keys(self.df['custom_fields_900007122446'][start_cnt])
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[2]/div[2]/div/div/div[9]/div[2]/div/input').send_keys(Keys.ENTER)
                time.sleep(0.5)
                logger.info(f'{start_cnt} 번째 --> CS | SLA 유형 --> 작업 완료')
            else:
                logger.info(f'{start_cnt} 번째 CS | SLA 유형가 비어 있습니다.')
        except Exception as e:  # except count --> 11
            logger.info(
                f'{start_cnt} 번째 --> 댓글모드 --> 작업 완료에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            start_cnt += 1
            pass
    def macro_create_click(self,start_cnt):
        # try 12 : 매크로 생성
        try:  # try count --> 12
            self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click()
            logger.info(f'{start_cnt} 번째 --> 모든  --> 작업을 완료하고 등록에 성공하였습니다.')

        except Exception as e:  # except count --> 12
            logger.info(f'{start_cnt} 번째 --> 모든  --> 작업을 중지하고 등록에 실패하였습니다.  :: error = {e}')
            self.create_error_list.append(start_cnt)
            pass
        start_cnt += 1
    def macro_complete_alarm(self):
        logger.info(f'{self.start_cnt_original} - {self.end_cnt} ~ {self.end_cnt}번째 작업을 완료하였습니다.')
        logger.info(f'{self.start_cnt_original} ~ {self.end_cnt}번 중 등록에 실패한 리스트입니다. :: create_error = {self.create_error_list}')

def crate_macro(cnt):
    zen = ZendeskEdit(cnt)
    zen.making_df()
    while cnt <= cnt + 10:
        zen.moving_site(cnt)
        zen.comment_update(cnt)
        zen.macro_name_update(cnt)
        zen.macro_subject_update(cnt)
        zen.category_update(cnt)
        zen.priority_update(cnt)
        zen.add_tag_update(cnt)
        zen.remove_tag_update(cnt)
        zen.pic_update(cnt)
        zen.comment_mode_update(cnt)
        zen.sla_update(cnt)
        zen.macro_create_click(cnt)
        zen.macro_complete_alarm(cnt)

if __name__=='__main__':
    # count_list = [0, 10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
    crate_macro(0)



    # count_list = [0]
    #     # pool = Pool(processes=1)
    #     # pool = Pool()
    #     # pool.map(crate_macro, count_list)
    crate_macro(0)

    # crawling_session(0)

