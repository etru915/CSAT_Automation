# 2021-08-31
# 등록된 매크로에서 사용 대상 그룹을 일괄로 변경하기
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

class ZendeskEditAccessUserUpdate:
    def __init__(self):
        self.df = pd.read_excel('C:/Users/zeno915/Desktop/upload_list.xlsx', header=0, usecols="a:n", index_col='no')
        time.sleep(5)
        logger.info(f'DF 생성 완료')
        self.create_error_list = []
        self.chrome_options = Options()
        self.chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        self.driver = webdriver.Chrome(executable_path='C:/PythonProjects/chromedriver.exe', chrome_options=self.chrome_options)
        self.driver.set_window_size(1500, 900)
        self.driver.implicitly_wait(15)

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
        self.driver.switch_to.frame('zendesk-clean-admin')
        logger.info(f'로그인 완료')

    def macro_open(self,start_cnt):
        try:
            time.sleep(2)
            logger.info(f'{start_cnt} > 작업 시작')
            self.driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/input').send_keys(self.df['macro.title'])
            logger.info(f'{start_cnt} > 제목입력 시작')
            self.driver.find_element_by_xpath('/html/body/div/div/section/div[3]/div[1]/div/div[2]').click()
            self.current_agent = self.driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[3]/a').text
            logger.info(f'{start_cnt}  > current_agent :  {self.current_agent}')
            if self.current_agent == "모든 상담원" :
                self.driver.find_element_by_xpath('/html/body/div/div/section/div[4]/table/tbody/tr/td[2]/a').click()
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/button').click()
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[1]/div/input').send_keys('그룹의 상담원\n')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div').click()
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('A_control-CREF')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('B_Test-ABR')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys('C_Test-AD')
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ARROW_DOWN)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[1]/fieldset[1]/span/div/div[2]/div/div[2]/div/input').send_keys(Keys.ENTER)
                self.driver.find_element_by_xpath('/html/body/div[1]/div/section/form/div[2]/button[2]').click() # 저장 버튼 클릭하기
                logger.info(f'{start_cnt} > 저장버튼 클릭 완료')
                self.driver.find_element_by_xpath('/html/body/div/div/section/div[1]/div[1]/div[2]').click() # 제목창에 내용 지우기
                logger.info(f'{start_cnt} & 번째 작업 완료')
                start_cnt += 1
            else:
                pass
        except Exception as e:
            self.driver.get("https://coupangcustomersupport.zendesk.com/agent/admin/macros")
            self.driver.switch_to.frame('zendesk-clean-admin')
            self.create_error_list.append(start_cnt)
            logger.info(f'{start_cnt} 번째 작업 실패  :: error = {e}')
            start_cnt += 1
            pass

    def result(self):
        logger.info(f'작업을 완료하였습니다.')
        logger.info(f'등록에 실패한 리스트입니다. :: create_error = {self.create_error_list}')

def start_macro(start_cnt):
    zen = ZendeskEditAccessUserUpdate()
    while start_cnt <= 100:
        zen.macro_open(start_cnt)
        start_cnt += 1
    zen.result()


if __name__=='__main__':
    count_list = [0]
    pool = Pool(processes=1)
    pool.map(start_macro, count_list)
