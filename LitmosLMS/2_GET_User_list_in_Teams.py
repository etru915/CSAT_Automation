# LMS 내 팀 내 포함된 인원들의 정보 가져오기

import requests
import json
import pandas as pd
from pandas import DataFrame
import time

url_value1 = "https://api.litmos.com/v1.svc/teams/"
url_value2 = ["aK1hr4srNBI1"] # 팀 ID
url_value3 = "/users?source=My-App&format=json&limit=1000"
apikey = '6e169a2d-ce5c-4f58-845f-14ff8416e4fa'
payload =""

headers= {'apikey':apikey , "Content-Type":"application/json"} #내 API 키

df_datas = []

for i in url_value2:
    response_value = requests.request("get",url_value1 + i + url_value3,  headers=headers, data = payload, verify=False)
    print("get ->" + i +" Team list status : " , response_value.status_code)
    data = json.loads(response_value.text)
    df = pd.json_normalize(data)
    df["Team ID"] = i
    df_datas.append(df)
    df_merge = pd.concat(df_datas,sort =False , ignore_index= True)
    df_final = DataFrame(df_merge)
    time.sleep(2)


df_final.to_excel("C://Users//zeno915//Desktop//Litmos LMS Users in Teams.xlsx")
