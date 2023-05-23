from litmos import Litmos


API_KEY = '6e169a2d-ce5c-4f58-845f-14ff8416e4fa'
LITMOS_APP_NAME = 'coupang.litmos.com'
LITMOS_SERVER_URL = 'https://api.litmos.com/v1.svc'  # https://support.litmos.com/hc/en-us/articles/227734667-Overview-Developer-API
litmos = Litmos(API_KEY, LITMOS_APP_NAME, LITMOS_SERVER_URL)

all_teams = litmos.Team.all()
for i in all_teams:
 print(i)