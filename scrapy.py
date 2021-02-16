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


    # print("CANCELAR")
    # import pdb; pdb.set_trace()
    # import pdb; pdb.set_trace()
    # import pdb; pdb.set_trace()
    # import pdb; pdb.set_trace()
    # import pdb; pdb.set_trace()
    # ##################################################################

    ua = UserAgent()
    sleep(random.randint(0,10)) 
    sleep(random.randint(0,10)) 
    response = requests.get(url, {"User-Agent": ua.random} )  
    if response.status_code != 200:
        sleep(random.randint(0,10)) 
        response = requests.get(url, headers=header.generate() ) 
    
    print (response.status_code)
    import pdb; pdb.set_trace()
    
    it_url = itemUrl()
    
    
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all('div', attrs = {'class': 'ZINbbc'})
    results=[re.search('\/url\?q\=(.*)\&sa',str(i.find('a', href = True)['href'])) for i in result]
    
    
    links=[i.group(1) for i in results if i != None]
    for x in results:
        if x != None:
            
            ignorar = session.query(UrlIgnorar).filter(UrlIgnorar.dominio.ilike(urlparse(x.group(1)).netloc.split('.')[1])).all()
                        
            if len(ignorar) == 0:
                
                ext = pathlib.Path(x.group(1)).suffix
                
                ignorarExtensoes = ['.xls','.xlsx', '.pdf', '.rar', '.exe']

                result = list(filter(lambda x: str(ext).lower() in x, ignorarExtensoes))  
                addUrl = UrlBase()
                if len(result) > 0:
                    addUrl.dominio = urlparse(x.group(1)).netloc
                    addUrl.url = urlparse(x.group(1)).scheme+"://"+urlparse(x.group(1)).netloc
                else:
                    addUrl.dominio = urlparse(x.group(1)).netloc
                    addUrl.url = x.group(1)
                
                session.add(addUrl)
                session.commit()
                # TODO: erro na inserção -- , autoincrement=True na criacaçõ da tabeça -> https://stackoverflow.com/questions/20848300/unable-to-create-autoincrementing-primary-key-with-flask-sqlalchemy
                
                it_url = itemUrl()
                it_url.url_id =addUrl.id
                it_url.item_pesquisa_id = item_pesquisa.id
                session.add(it_url)
                
                
    session.commit()
    
    
    
    
    return (links)    




def getDados():
    # TODO:  Pendente
    pass