import requests  # aqui
import re
import urllib
from urllib.parse import urlparse, urlsplit
from bs4 import BeautifulSoup
# from requests.models import Response # aqui
from migrate import session,UrlBase,UrlIgnorar,itemUrl,ItemPesquisa
from fake_headers import Headers
from fake_useragent import UserAgent
import pathlib
from time import sleep # aqui
import random # aqui
# import nltk
import util
import json
from collections import deque 
import numpy as np

header = Headers(
        headers=True
    )

"""[summary] 
Efetuar pesquisa no google e armazena no banco de dados as Url's 
[params]
    busca = String (palavra chave)
    n_resultados = Int ( quantidade de resultados por pagina, default 3000)
"""
def getUrls(busca,n_results=3000):
    busca = urllib.parse.quote_plus(busca)
    n_results = int(n_results)

    url = "https://www.google.com/search?q=" + busca + "&num=" + str(n_results)
    
    item_pesquisa = ItemPesquisa()
    item_pesquisa.item = busca
    session.add(item_pesquisa)
    session.commit()

    response = util.getRequest(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    
    links = [a['href'] for a in soup.find_all('a', href=True)]
    for i in links:
        if i.startswith('https') or i.startswith('http'):
            ignorar = session.query(UrlIgnorar).\
                filter(UrlIgnorar.dominio == urlparse(i).scheme+"://"+urlparse(i).netloc)\
                    .all() 
            if len(ignorar) == 0:
                url = urlparse(i).scheme+"://"+urlparse(i).netloc
                results.append(url)
    
    
    semDuplicados = np.unique(results).tolist()
    
    for i in semDuplicados:
        if i.find('blog') == -1: #removendo url de blog
            addUrl = UrlBase()
            addUrl.dominio = i
            addUrl.url = i
            session.add(addUrl)
            session.commit()

            it_url = itemUrl()
            it_url.url_id =addUrl.id
            it_url.item_pesquisa_id = item_pesquisa.id
            session.add(it_url)
    

    session.commit()
    return (item_pesquisa.id) 
    
    
def pesquisa(busca):
    
    item_pesquisa = getUrls(busca)
    getDados(item_pesquisa)

    
    # getDados(1)

    return "aui"




def getDados(item_pesquisa):

    VARRER_TODO_SITE =  False
    processed_urls = set() 
    emails = set()  

    result = session.query(UrlBase)\
        .join(itemUrl,UrlBase.id == itemUrl.url_id)\
        .filter(itemUrl.item_pesquisa_id== item_pesquisa)\
        .all()

    # result = session.query(UrlBase)\
    #     .filter(UrlBase.id == 18 )\
    #     .distinct()\
    #     .all()
        # .filter(UrlBase.cnpj == "" and UrlBase.telefone_fixo == "" and UrlBase.telefone_celular == "" and UrlBase.cep == "")\
        # .filter(UrlBase.dominio == 'www.cofermeta.com.br')\
        
    for row in result:
        new_urls = deque([row.url])
        while len(new_urls):  
            url = new_urls.popleft()  
            processed_urls.add(url)  

            response = util.getRequest(url)    
            print("############################")    
            print(response)
            if response:
                parts = urlsplit(url)
                
                base_url = "{0.scheme}://{0.netloc}".format(parts)  
                path = url[:url.rfind('/')+1] if '/' in parts.path else url     
                
                email = util.regex('email',response.text)
                if email is not None and email != '[]':
                    session.query(UrlBase).filter(UrlBase.id == row.id).update({"email": email})
                
                
                cnpj = util.regex('cnpj',response.text)
                if cnpj is not None and cnpj != '[]':
                    session.query(UrlBase).filter(UrlBase.id == row.id).update({"cnpj": cnpj})
                    try:
                        session.query(UrlBase).filter(UrlBase.id == row.id).update({"dados_cnpj": str(getDadosCNPJ(cnpj))})
                    except:
                        pass

                cep = util.regex('cep',response.text)
                if cep is not None and cep != '[]':
                    session.query(UrlBase).filter(UrlBase.id == row.id).update({"cep": cep})
                    try:
                        aux = json.loads(cep)
                        if len(aux) > 0:
                            endereco = []
                            for i in aux:
                                end = getDadosCEP(parse_input(i))
                                if not "erro" in end:
                                    endereco.append(end)
                        
                        session.query(UrlBase).filter(UrlBase.id == row.id).update({"endereco": json.dumps(endereco)})
                    except:
                        pass
                
                
                fixo =util.regex('telefone',response.text) 
                if fixo is not None and fixo != '[]':
                    session.query(UrlBase).filter(UrlBase.id == row.id).update({"telefone_fixo": fixo})
                    
                celularAPI =util.regex('telefoneAPI',response.text) 
                if celularAPI is not None and celularAPI != '[]':
                    if celularAPI is not None:
                        z = []
                        celularAPI = json.loads(celularAPI)
                        for i in celularAPI:
                            if i[:3] == '=55':
                                z.append(i[1:])
                        z = json.dumps(z)                        
                        session.query(UrlBase).filter(UrlBase.id == row.id).update({"telefone_celular": z })
                
                    
                    
                session.commit()

        
                soup = BeautifulSoup(response.text ,"html.parser")
                
                for anchor in soup.find_all("a"):  
                    link = anchor.attrs["href"] if "href" in anchor.attrs else ''  
                    if link.startswith('/'):  
                        link = base_url + link  
                    elif not link.startswith('http'):  
                        link = path + link  
                    if not link in new_urls and not link in processed_urls and VARRER_TODO_SITE:  
                        print(link)
                        aux = urlparse(link)
                        if row.dominio == aux.netloc :
                            new_urls.append(link)  
            else:
                continue
     
     
def getDadosCEP(cep):
    url = ('http://www.viacep.com.br/ws/%s/json' % cep)
    
    req = util.getRequest(url) 
    if req.status_code == 200:
        dados_json = json.loads(req.text)
        return dados_json

def parse_input(i):
    'Retira caracteres de separação do CNPJ'
    i = str(i)
    i = i.replace('.', '')
    i = i.replace(',', '')
    i = i.replace('/', '')
    i = i.replace('-', '')
    i = i.replace('\\', '')
    i = i.replace('"', '')
    i = i.replace('[', '')
    i = i.replace(']', '')
    i = i.replace(' ', '')
    i = i.replace("'","")
    
    return i

def getDadosCNPJ(cnpj):
    cnpj = parse_input(cnpj)

    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    req = util.getRequest(url)  
    if req.status_code == 200:
        return json.loads(req.text)
   

# Adicionar Url na tabela URL_IGNORAR
def addUrlIgnorar(url):
    for i in url:    
        url_ignorar = UrlIgnorar()
        url_ignorar.dominio = i if i[-1] != '/' else i[:-1]
        session.add(url_ignorar)
        session.commit()
    