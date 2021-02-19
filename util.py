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
        'email':r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+',
        'cep': 'CEP\s*(\d{5})-(\d{3})',
        'cnpj': '\d{2}.\d{3}.\d{3}/\d{4}-\d{2}',
        'telefone': '(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})',
        'telefone2': r'\+[\d]{2}\D*[\d]{2}\D*[\d]{4,5}\D*[\d]{4}',
        'telefoneAPI': r"\+?[\d]{2}\s*[\d]{2}\s*[\d]{4,5}\s*[\d]{4}"
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
       