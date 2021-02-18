# import requests
# from bs4 import BeautifulSoup
# from fake_headers import Headers
# from time import sleep
# import random
# header = Headers(
#         browser="firefox",
#         os="win",
#         headers=True
#     )


# url ='https://www.google.com/search?q=bbb'
# # url ='https://duckduckgo.com/?q=rolamentos&t=h_&ia=web'
# from fake_useragent import UserAgent

# ua = UserAgent()

# sleep(random.randint(0,10)) 
# req = requests.get(url, {"User-Agent": ua.random} )  
# print(req)
# if req.status_code != 200:
#     sleep(random.randint(0,10)) 
#     req = requests.get(url, headers=header.generate() ) 
#     print(req)
    
    
    
    
# # req = requests.get(url, {"User-Agent": ua.random})
# # soup = BeautifulSoup(req.content, 'html.parser')
# # # print(soup.prettify())
# # print(soup.find_all("a"))


# # import pandas as pd
# # import numpy as np
# # import urllib
# # from fake_useragent import UserAgent
# # import requests
# # import re
# # from urllib.request import Request, urlopen
# # from bs4 import BeautifulSoup

# # keyword= "rolamentos"
# # html_keyword= urllib.parse.quote_plus(keyword)
# # print(html_keyword)

# # number_of_result=20
# # google_url = "https://www.google.com/search?q=" + html_keyword + "&num=" + str(number_of_result)
# # print(google_url)


# # ua = UserAgent()
# # response = requests.get(google_url, {"User-Agent": ua.random})
# # soup = BeautifulSoup(response.text, "html.parser")

# # result = soup.find_all('div', attrs = {'class': 'ZINbbc'})
# # results=[re.search('\/url\?q\=(.*)\&sa',str(i.find('a', href = True)['href'])) for i in result]
# # #this is because in rare cases we can't get the urls
# # links=[i.group(1) for i in results if i != None]
# # links


# # goog_search = url

# # r = requests.get(goog_search)
# # soup = BeautifulSoup(r.text)
# # import pdb; pdb.set_trace()
# # for link in soup.find_all("a"):
# #     print ("++===== = "+link.get("href"))
# # import pdb; pdb.set_trace()


import asyncio
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def run(r):
    # url = "http://localhost:8080/{}"
    url = "https://www.soesferas.com.br/esferas-aco-rolamentos"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)

def print_responses(result):
    print(result)
    print("foi esse")

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4))
loop.run_until_complete(future)