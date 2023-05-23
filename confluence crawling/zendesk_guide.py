import requests
from bs4 import BeautifulSoup

url = "https://support.coupang.com/hc/ko/articles/900002013683"

response = requests.get(url)
print(response.status_code )
response.text

soup = BeautifulSoup(response.text, 'html.parser')