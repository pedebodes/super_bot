import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from time import sleep
import random
header = Headers(
        browser="firefox",
        os="win",
        headers=True
    )


url ='https://www.google.com/search?q=bbb'
# url ='https://duckduckgo.com/?q=rolamentos&t=h_&ia=web'
from fake_useragent import UserAgent

ua = UserAgent()

sleep(random.randint(0,10)) 
req = requests.get(url, {"User-Agent": ua.random} )  
print(req)
if req.status_code != 200:
    sleep(random.randint(0,10)) 
    req = requests.get(url, headers=header.generate() ) 
    print(req)
    
    
    
    
# req = requests.get(url, {"User-Agent": ua.random})
soup = BeautifulSoup(req.content, 'html.parser')
# print(soup.prettify())
print(soup.find_all("a"))


# import pandas as pd
# import numpy as np
import urllib
from fake_useragent import UserAgent
import requests
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# keyword= "rolamentos"
# html_keyword= urllib.parse.quote_plus(keyword)
# print(html_keyword)

# number_of_result=20
# google_url = "https://www.google.com/search?q=" + html_keyword + "&num=" + str(number_of_result)
# print(google_url)


# ua = UserAgent()
# response = requests.get(google_url, {"User-Agent": ua.random})
# soup = BeautifulSoup(response.text, "html.parser")

# result = soup.find_all('div', attrs = {'class': 'ZINbbc'})
# results=[re.search('\/url\?q\=(.*)\&sa',str(i.find('a', href = True)['href'])) for i in result]
# #this is because in rare cases we can't get the urls
# links=[i.group(1) for i in results if i != None]
# links


# goog_search = url

# r = requests.get(goog_search)
# soup = BeautifulSoup(r.text)
# import pdb; pdb.set_trace()
for link in soup.find_all("a"):
    print ("++===== = "+link.get("href"))
import pdb; pdb.set_trace()



