from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote_plus
from urllib.request import urlretrieve
import requests

link = 'https://kms.coupang.net/pages/viewpage.action?pageId=4391357'

# req = requests.get(link)
req = urlopen(link).read()

soup = BeautifulSoup(req,"html.parser")

# new_file =  open("C:/Users/zeno915/Desktop/pycharm/1.html",'w',encoding= 'utf-8')
# new_file.write(req.text)
# new_file.close()

img_list = soup.find_all(class_="confluence-embedded-image")



for i in img_list:
    href = i.attrs['src']
    print(href)
img_src = "https://kms.coupang.net/download/attachments/4391357/%EA%B7%B8%EB%A6%BC1.png?version=2&modificationDate=1568769901000&api=v2"
urlretrieve(img_src, "C:/Users/zeno915/Desktop/pycharm/img_test.png")
# print(req.text)
