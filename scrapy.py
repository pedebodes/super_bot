import requests
import re
import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from migrate import session,UrlBase,UrlIgnorar,itemUrl,ItemPesquisa
from fake_headers import Headers
from fake_useragent import UserAgent
import pathlib
from time import sleep
import random
import nltk

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


    ua = UserAgent()
    sleep(random.randint(0,10)) 
    sleep(random.randint(0,10)) 
    response = requests.get(url, {"User-Agent": ua.random} )  
    if response.status_code != 200:
        sleep(random.randint(0,10)) 
        response = requests.get(url, headers=header.generate() ) 
    
    it_url = itemUrl()
    
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all('div', attrs = {'class': 'ZINbbc'})
    
    results = []
    for i in result:
        ln = i.find('a', href = True)            
        if ln is not None:
            results.append(re.search('\/url\?q\=(.*)\&sa',str(ln['href'])))
    results = res = [i for i in results if i] 
    
    links=[i.group(1) for i in results if i != None]
    for x in results:
        if x != None:

            ul =urlparse(x.group(1)).netloc.split('.')[0]
            if ul == 'www':
                ul =urlparse(x.group(1)).netloc.split('.')[1]

            ignorar = session.query(UrlIgnorar).filter(UrlIgnorar.dominio.ilike(ul)).all()
            if len(ignorar) == 0:
                
                ext = pathlib.Path(x.group(1)).suffix
                
                ignorarExtensoes = ['.xls','.xlsx', '.pdf', '.rar', '.exe']

                result = list(filter(lambda x: str(ext).lower() in x, ignorarExtensoes))  
                
                addUrl = UrlBase()
                if bool(urlparse(x.group(1)).netloc.strip()):
                    if len(result) > 0:
                        addUrl.dominio = urlparse(x.group(1)).netloc
                        addUrl.url = x.group(1)
                    else:
                        addUrl.dominio = urlparse(x.group(1)).netloc
                        addUrl.url = urlparse(x.group(1)).scheme+"://"+urlparse(x.group(1)).netloc

                    session.add(addUrl)
                    session.commit()
                
                    it_url = itemUrl()
                    it_url.url_id =addUrl.id
                    it_url.item_pesquisa_id = item_pesquisa.id
                    session.add(it_url)
                    
                
    session.commit()
    return (links)    

    
def pesquisa(busca):
    ignorar = session.query(ItemPesquisa).all()
    
    id_similares = []
    for i in ignorar:
        # verifica distancia de similaridade da palavra buscada
        x = nltk.edit_distance(str(busca), i.item)
        if x < 3:
            id_similares.append(i.id)
    
    if len(id_similares) > 0:
        # TODO: PENDETE 
        
        return getUrls(busca) # isso vai sair daqui
    else:
        print("Busca o pelo nome")
        # return getUrls(busca)
        return getUrls(busca)




def getDados():
    # TODO:  Pendente
    pass

