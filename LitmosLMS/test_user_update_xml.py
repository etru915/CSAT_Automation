import requests
import json
import pandas as pd

url_team = "https://api.litmos.com/v1.svc/users/HqmNmMOfrNS_64f4baY9Aw2?source=My-App"

payload ="""
    <User> 
        <Id>HqmNmMOfrNS_64f4baY9Aw2</Id> 
        <UserName>JJ001855@coupartners.com</UserName> 
        <FirstName>JJ001855</FirstName> 
        <LastName>JJ001855</LastName> 
        <FullName></FullName> 
        <Email>JJ001855@coupartners.com</Email> 
        <AccessLevel>Learner</AccessLevel> 
        <DisableMessages>false</DisableMessages> 
        <Active>true</Active> 
        <LastLogin></LastLogin> 
        <LoginKey></LoginKey> 
        <IsCustomUsername>true</IsCustomUsername> 
        <SkipFirstLogin>false</SkipFirstLogin> 
        <TimeZone></TimeZone> 
        </User>
    """

headers= {'apikey':'ab1dd438-17ce-4309-9d3a-622761ee56a0' , "Content-Type":"application/xml"} #내 API 키
# response = requests.request("delete", url_team_kill, headers=headers, data = payload, verify=False)
response1 = requests.request("put",url_team,  headers=headers, data = payload, verify=False)
print(response1.status_code)


"""
{
"Id":"HqmNmMOfrNS_64f4baY9Aw2" ,
"UserName": "JJ001855@coupartners.com",
"FirstName":"MyFirstName",
"LastName":"MyLastName",
"FullName":"",
"Email":"JJ001855@coupartners.com",
"AccessLevel":"Learner",
"DisableMessages":"false",
"Active":"true",
"LastLogin":"",
"LoginKey":"",
"IsCustomUsername":"true",
"SkipFirstLogin":"false",
"TimeZone":""
}"""