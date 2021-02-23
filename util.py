import requests
from requests.exceptions import HTTPError
from fake_headers import Headers
from time import sleep
import random
import re
import json
from fake_useragent import UserAgent


def removeDuplicado(valor):
    return list(dict.fromkeys(valor))
    
def regex(opcao,arquivo):
    tipoRegex={
        'email':re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+'),
        'cep': re.compile(r'\s+(\d{5})[- ](\d{3})\s*'),
        'cnpj': re.compile(r'\d{2}.\d{3}.\d{3}/\d{4}-\d{2}'),
        'telefone': re.compile(r'\+?5?5?[\-\.\s]*\(?(\d{2})\)?\s+(\d{4,5})[-. ]?(\d{4})'),
        'telefoneAPI': re.compile(r'\=+[\d]{13}\&+')
        }
    
    return json.dumps(
        removeDuplicado(
            re.findall(
                tipoRegex.get(opcao), arquivo
                )
            )
        )
    

    
def getRequest(url):
    try:
        header = Headers(
            headers=True
        )
        sleep(random.randint(2,30)) 
        return requests.get(url, headers=header.generate()) # timeout=5,verify = False
        # ua = UserAgent()
        # sleep(random.randint(2,30)) 
        # response = requests.get(url, {"User-Agent": ua.random} )  
        # if response.status_code != 200:
        #     sleep(random.randint(2,30)) 
        #     response = requests.get(url, headers=header.generate() ) 
        # return response

    except HTTPError as http_err:
        print(f'Erro HTTP: {http_err}')
        return False
    except Exception as err:
        print(f'Outro erro desconhecido: {err}')    
        return False
    except:
        print('Erro indefinido')
        return False
       