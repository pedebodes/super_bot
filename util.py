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
    
    return re.findall(tipoRegex.get(opcao), arquivo)
    
            
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
            headers=False
        )
        sleep(random.randint(2,30)) 
        return requests.get(url, headers=header.generate(),timeout=5) # timeout=5,verify = False
        
    except requests.exceptions.RequestException as err:
        return err
    except requests.exceptions.HTTPError as errh:
        return errh
    except requests.exceptions.ConnectionError as errc:
        return errc
    except requests.exceptions.Timeout as errt:
        return errt
    
    
    # try:
    #     header = Headers(
    #         headers=False
    #     )
    #     sleep(random.randint(2,30)) 
    #     return requests.get(url, headers=header.generate())


    # except HTTPError as http_err:
    #     return (f'Erro HTTP: {http_err}')
        
    # except Exception as err:
    #     return (f'Site fora do ar ou nao responde: {err}')    
    #     return False
    # except:
    #     return ('Erro indefinido')
    #     return False

def parse_input(i):
    return ''.join(x for x in i if x.isdigit())

