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
from sqlalchemy import func

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
    sleep(random.randint(2,30)) 
    response = requests.get(url, {"User-Agent": ua.random} )  
    if response.status_code != 200:
        sleep(random.randint(2,30)) 
        response = requests.get(url, headers=header.generate() ) 

    # response = util.getRequest(url)
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

            ignorar = session.query(UrlIgnorar)\
                .filter(UrlIgnorar.dominio == urlparse(x.group(1)).scheme+"://"+urlparse(x.group(1)).netloc)\
                    .all() 
            
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
    
    # Removendo registros duplicados
    result = session.query(UrlBase)\
    .group_by(UrlBase.dominio)\
    .having(func.count(UrlBase.dominio) > 1)\
    .all()
    for i in result:
        session.query(UrlBase).filter(UrlBase.id==i.id).delete()
    session.commit()
    
    return (item_pesquisa.id)    
    

    
def pesquisa(busca):
    item_pesquisa = getUrls(busca)
    # getDados(item_pesquisa)
    
    
    return "aui"




def getDados(item_pesquisa):

    VARRER_TODO_SITE =  False
    processed_urls = set() 
    emails = set()  

    # result = session.query(UrlBase)\
    #     .filter(UrlBase.id == 1 )\
    #     .distinct()\
    #     .all()
        # .filter(UrlBase.dominio == 'www.cofermeta.com.br')\

    result = session.query(UrlBase)\
        .join(itemUrl,UrlBase.id == itemUrl.url_id)\
        .filter(itemUrl.item_pesquisa_id== item_pesquisa)\
        .all()
        
    for row in result:
        new_urls = deque([row.url])
        while len(new_urls):  
            url = new_urls.popleft()  
            processed_urls.add(url)  

            response = util.getRequest(url)    
            print("############################")    
            print(response)
            if response:
                if response.status_code != 200:#403 404
                    print("DEU ERRO")
                    import pdb; pdb.set_trace()
                print("############################")    
                parts = urlsplit(url)
                # ua.update()
                
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
                        endereco = getDadosCEP(parse_input(cep))
                        if not "erro" in endereco:
                            session.query(UrlBase).filter(UrlBase.id == row.id).update({"endereco": endereco})
                    except:
                        pass

                fixo =util.regex('telefone',response.text) 
                if fixo is not None and fixo != '[]':
                    session.query(UrlBase).filter(UrlBase.id == row.id).update({"telefone_fixo": fixo})
                    
                
                celularAPI =util.regex('telefoneAPI',response.text) 
                if celularAPI is not None and celularAPI != '[]':
                    celularAPI = celularAPI if celularAPI[:2] == '55' else None
                    if celularAPI is not None:
                        session.query(UrlBase).filter(UrlBase.id == row.id).update({"telefone_celular": celularAPI })
                
                # celular =getCelular(response.text) 
                                                        
                # if celular is not None:
                #     session.query(UrlBase).filter(UrlBase.id == row.id).update({"telefone_celular": celular })
                    
                    
                    
                session.commit()

        
                soup = BeautifulSoup(response.text ,"html.parser") #lxml
                
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
                # TODO: incluir a na url caso não retorne nada , ou seja entrou aqui
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
    
    return i

def getDadosCNPJ(cnpj):
    cnpj = parse_input(cnpj)

    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    req = util.getRequest(url)  
    if req.status_code == 200:
        return json.loads(req.text)
   

# Adicionar Url na tabela URL_IGNORAR
def addUrlIgnorar(url):
    
    url_ignorar = UrlIgnorar()
    url_ignorar.dominio = url
    session.add(url_ignorar)
    session.commit()

    return "Adicionado com sucesso"
    
    