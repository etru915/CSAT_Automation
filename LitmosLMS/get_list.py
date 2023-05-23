import requests
import json
import pandas as pd


class Get_list():
    def __init__(self):
        self.base_url = "https://api.litmos.com/v1.svc/"
        self.apikey = {'apikey':'3aebcb1a-fbe3-4c08-9aac-cda38c636833'}
    def user_list(self):
        self.main_url = "users?source=MY-APP&limit=1000&format=json"
        self.payload={}
        self.headers = {self.apikey}
        self.response = requests.request("GET", self.base_url+self.main_url , headers=headers, data=payload)
        self.result = response.text.encode('utf8')




url = "https://api.litmos.com/v1.svc/users?source=MY-APP&limit=1000&format=json"

# url = "https://api.litmos.com/v1.svc/users/S9dZexyug9_qe2ALtWq9Rg2?source=MY-APP&limit=1000&format=json" - id로 사람 정보 찾아오기
# url = "https://api.litmos.com/v1.svc/users/U000778@coupartners.com?source=MY-APP&limit=1000&format=json" - ID로 사람 정보 찾아오기
payload = {}
headers= {'apikey':'3aebcb1a-fbe3-4c08-9aac-cda38c636833'}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))

data = json.loads(response.text.encode('utf8'))

df = pd.json_normalize(data)
print(df)
