import requests
from requests.exceptions import HTTPError
from fake_headers import Headers
# from fake_useragent import UserAgent
from time import sleep
import random
def getRequest(url):
    try:
        header = Headers(
            headers=True
        )
        sleep(random.randint(2,30)) 
        return requests.get(url, headers=header.generate() , timeout=5,verify = False) #verify = Falseasas
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return False
    except Exception as err:
        print(f'Other error occurred: {err}')    
        return False
    except:
        return False
        print('An exception occurred')
       
       
