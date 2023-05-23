import requests
import json
import pandas as pd

url_team = "https://api.litmos.com/v1.svc/teams/NQYf93KaW981/users?source=My-App"

payload ="""
 [{
 "Id":"HqmNmMOfrNS_64f4baY9Aw2",
 "UserName": "",
 "FirstName": "",
 "LastName": ""
 }, {
 "Id":"2IoDtf-peLjlxoLNj42iaw2",
 "UserName": "",
 "FirstName": "",
 "LastName": ""
 }]
"""

headers= {'apikey':'ab1dd438-17ce-4309-9d3a-622761ee56a0' , "Content-Type":"application/json"} #내 API 키
# response = requests.request("delete", url_team_kill, headers=headers, data = payload, verify=False)
response1 = requests.request("post",url_team,  headers=headers, data = payload, verify=False)
print(response1.status_code)
print(response1.text)