from litmos import Litmos


API_KEY = 'ab1dd438-17ce-4309-9d3a-622761ee56a0'
LITMOS_APP_NAME = 'coupang.litmos.com'
LITMOS_SERVER_URL = 'https://api.litmos.com/v1.svc'  # https://support.litmos.com/hc/en-us/articles/227734667-Overview-Developer-API
litmos = Litmos(API_KEY, LITMOS_APP_NAME, LITMOS_SERVER_URL)

# all_users = litmos.User.all()

print(litmos.litmos_api.api_key)
li = litmos.litmos_api.all("user")
print(li)
