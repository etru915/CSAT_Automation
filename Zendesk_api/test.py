import requests

# Set the request parameters
url = 'https://coupangcustomersupport.zendesk.com/api/v2/macros.json?include=usage_30d,usage_7d&page=1'
user = 'zeno915@coupang.com'
pwd = 'jjangkyo21!!'

# Do the HTTP get request
response = requests.get(url, auth=(user, pwd), verify=False)

if response.status_code != 200:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
    exit()