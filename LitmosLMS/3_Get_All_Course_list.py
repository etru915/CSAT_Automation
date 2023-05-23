# LMS 내 모든 코스 정보 가져오기

import requests
import json
import pandas as pd
from pandas import DataFrame
import time

url_value1 = "https://api.litmos.com/v1.svc/courses?source=My-App&format=json&limit=1000"

apikey = '6e169a2d-ce5c-4f58-845f-14ff8416e4fa'
payload =""
headers= {'apikey':apikey , "Content-Type":"application/json"} #내 API 키

response_value = requests.request("get",url_value1,  headers=headers, data = payload, verify=False)

print("get All Courses list status : " , response_value.status_code)

data = json.loads(response_value.text)
df = pd.json_normalize(data)
df.to_excel("C://Users//zeno915//Desktop//Litmos LMS All Course List.xlsx")
