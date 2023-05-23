import requests
import csv
import unicodedata

# Set the request parameters
# Change the URL according to what information is desired.
url = 'https://coupangcustomersupport.zendesk.com/api/v2/help_center/en-us/articles.json?sort_by=title&sort_order=asc'

# Use Your Zendesk Support Sign-On Credentials
user = 'zeno915'
pwd = 'jkh8209$#'

# Path of the outputted csv file
csvfile = 'C:/Users/zeno915/Desktop/pycharm/filename.csv'

# This loop cycles through all pages of articles, converts the unicode
# to an integer, and writes the integers to an array
output = []
while url:
        response = requests.get(url, auth = (user, pwd))
        data = response.json()
        for article in data['articles']:
                article_url = article['html_url']
                decode = unicodedata.normalize('NFKD', article_url).encode('ascii','ignore')
                output.append(decode)
        print(data['next_page'])
        url = data['next_page']

# Print number of articles
print("Number of articles:")
print (len(output))

#Write to a csv file
with open(csvfile, 'w') as fp:
    writer = csv.writer(fp, dialect = 'excel')
    writer.writerows([output])