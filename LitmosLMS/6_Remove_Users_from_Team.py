# LMS 내 특정 팀에 포함된 인원들 한번에 제거하기

import requests
import json
import pandas as pd
from pandas import DataFrame
import time

url_value1 = "https://api.litmos.com/v1.svc/teams/KmgLZLW5IQY1/users/" # 제거 대상 팀 ID
url_value2 = ["Ifa7ct7XaGZcBLDh1kJ4mQ2","LgZ1DKhVGaVYchmg5JIe-w2",] # 제거 대상 사용자 ID

url_value3 = "?source=My-App"
apikey = '6e169a2d-ce5c-4f58-845f-14ff8416e4fa'
payload =""

headers= {'apikey':apikey , "Content-Type":"application/json"} #내 API 키

log_data = []

for i in url_value2:
    response_value = requests.request("delete",url_value1 + i + url_value3,  headers=headers, data = payload, verify=False)
    print("Delete ->" + i +" Delete Agent status : " , response_value.status_code)
    log_data.append("Delete ->" + i + " Delete Agent status : " + str(response_value.status_code))
    time.sleep(1)

with open('C://Users//zeno915//Desktop//user remove state.txt',"w") as log_file:
    for i in log_data:
        log_file.write(str(i)+"\n")