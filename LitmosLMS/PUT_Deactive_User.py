import requests
import json
import pandas as pd
from pandas import DataFrame
import time

url_value1 = "https://api.litmos.com/v1.svc/courses/"
url_value2 = ["9nyyeXOvU7M1", "rh5sKQhYGJQ1","I6nEf9b33XU1","z2w0TuvTcms1","Os-1bnTK9_U1"] # 코스 ID
url_value3 = "/modules?source=My-App&format=json&limit=1000"
apikey = '6e169a2d-ce5c-4f58-845f-14ff8416e4fa'

payload ="""
 {
 "CourseId":"HqmNmMOfrNS_64f4baY9Aw2",
 "UserId": "",
 "Score": "100",
 "Completed": "",
 "UpdatedAt":"",
  "Note":"staff_auto_completion",
   "Attempts":"1"
 }
"""

headers= {'apikey':apikey , "Content-Type":"application/json"} #내 API 키

df_datas = []
payload_all = []

for i in url_value2:
    response_value = requests.request("get",url_value1 + i + url_value3,  headers=headers, data = payload, verify=False)
    print("get ->" + i +" Module list status : " , response_value.status_code)
    data = json.loads(response_value.text)
    df = pd.json_normalize(data)
    df["Team ID"] = i
    df_datas.append(df)
    df_merge = pd.concat(df_datas,sort =False , ignore_index= True)
    df_final = DataFrame(df_merge)
    time.sleep(2)


df_final.to_excel("C://Users//zeno915//Desktop//Litmos LMS Modules in Courses.xlsx")
