# import requests
# from lxml.html import fromstring
# from itertools import cycle
# import traceback
# def get_proxies():
#     url = 'https://free-proxy-list.net/'
#     response = requests.get(url)
#     parser = fromstring(response.text)
   
#     proxies = set()
#     for i in parser.xpath('//tbody/tr')[:10]:
#         if i.xpath('//*[@id="proxylisttable"]'): 
            
#             #Grabbing IP and corresponding PORT
#             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#             proxies.add(proxy)
#     return proxies



# # proxies = get_proxies()
# # print(proxies)

# proxies = get_proxies()
# proxy_pool = cycle(proxies)

# url = 'https://httpbin.org/ip'
# for i in range(1,11):
#     #Get a proxy from the pool
#     proxy = next(proxy_pool)
#     print("Request #%d"%i)
#     try:
#         response = requests.get(url,proxies={"http": proxy, "https": proxy})
#         print(response.json())
#     except:
#         #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
#         #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
#         print("Skipping. Connnection error")



# # import random

# # foo = ['a', 'b', 'c', 'd', 'e']
# # print(random.choice(foo))



# # import requests
# # url = 'https://httpbin.org/ip'
# # # proxies = {
# # #     "http": 'http://209.50.52.162:9050', 
# # #     "https": 'http://209.50.52.162:9050'
# # # }
# # response = requests.get(url,proxies=proxies)
# # print(response.json())


from fake_headers import Headers

header = Headers(
        browser="chrome",  # Generate only Chrome UA
        # os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )




print (header.generate())

import viacep

d = viacep.ViaCEP('32010040') #32010040
data = d.getDadosCEP()
# print (data['erro'])
print(type(data))
if not "erro" in data:
    print("bosta")