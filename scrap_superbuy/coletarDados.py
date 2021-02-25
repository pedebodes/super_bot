from bs4 import BeautifulSoup  
import requests  
import requests.exceptions  
from fake_useragent import UserAgent
from urllib.parse import urlsplit  
from collections import deque  
import re  
from tabelas import engine, Resultados,session
from urllib.parse import urlparse
import random
from fake_headers import Headers
import viacep
from time import sleep
from consulta_cnpj import consulta
header = Headers(
        browser="chrome",
        # os="win",
        headers=True
    )


VARRER_TODO_SITE =  False


processed_urls = set() 


emails = set()  

result = session.query(Resultados)\
    .distinct()\
    .all()
    # .filter(Resultados.dominio == 'www.cofermeta.com.br')\
    # .filter(Resultados.id == 2 )\

#13  15 26 51
        
def getEmail(part1, part2):
    try:
        return list(
            dict.fromkeys(
                re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", part1, part2)
                )
            )
    except:
        return None

def getCnpj(part1):
    try:
        return re.search("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}", part1).group()
    except:
        return None
      
    pass
def getTelefoneFixo(part1):
    try:
      return re.search('\(\d{2}\) \s\d{4}\-\d{4}', part1).group()
    except:
        return None
    
def getCelular(part1):
    try:
        return re.search('\(\d{2}\) \s\d{5}\-\d{4}', part1).group()
    except:
        return None
def getCelularAPI(part1):
    try:
        return re.search('\d{13}', part1).group()
    except:
        return None
      
def getCep(part1):
    try:
        return re.search(r"CEP: \d{5}.\d{3}", part1).group()
    except:
        return None
def getCep1(part1):
    try:
        return re.search(r"\d{5}-\d{3}", part1).group()
    except:
        return None


for row in result:
    new_urls = deque([row.url])
    while len(new_urls):  
        url = new_urls.popleft()  
        processed_urls.add(url)  
        ua = UserAgent(cache=False)
        # url = "https://rolamentoscbf.com.br/"
        print("Processando %s" % url)  

        try:  
            sleep(random.randint(0,10)) 
            # headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
            # response = requests.get(url, headers=headers )  
            response = requests.get(url, {"User-Agent": ua.random} )  
            if response.status_code != 200:
                sleep(random.randint(0,10)) 
                response = requests.get(url, headers=header.generate() ) 
                    
                
            parts = urlsplit(url)
            ua.update()
            
            base_url = "{0.scheme}://{0.netloc}".format(parts)  
            path = url[:url.rfind('/')+1] if '/' in parts.path else url     
            
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))  
            emails.update(new_emails)  
            

            email = getEmail(response.text, re.I)
            if email is not None and len(email) > 0:
                session.query(Resultados).filter(Resultados.id == row.id).update({"email": str(email)})
            
            cnpj = getCnpj(response.text)
            if cnpj is not None:
                session.query(Resultados).filter(Resultados.id == row.id).update({"cnpj": cnpj})
                try:
                    session.query(Resultados).filter(Resultados.id == row.id).update({"dados_cnpj": str(consulta(cnpj))})
                except:
                    pass


            cep = getCep1(response.text)
            if cep is not None:
                session.query(Resultados).filter(Resultados.id == row.id).update({"cep": cep})
                try:
                    d = viacep.ViaCEP(cep.replace("-","").replace(".",""))
                    endereco = d.getDadosCEP()
                    if not "erro" in endereco:
                        session.query(Resultados).filter(Resultados.id == row.id).update({"endereco": str(endereco)})
                except:
                    pass
                
            cep = getCep(response.text)
            if cep is not None:
                session.query(Resultados).filter(Resultados.id == row.id).update({"cep": cep.split()[1]})
                try:
                    d = viacep.ViaCEP(cep.replace("-","").replace(".",""))
                    endereco = d.getDadosCEP()
                    if not "erro" in endereco:
                        session.query(Resultados).filter(Resultados.id == row.id).update({"endereco": str(endereco)})
                except:
                    pass
                
                

            fixo =getTelefoneFixo(response.text)  
            if fixo is not None:
                session.query(Resultados).filter(Resultados.id == row.id).update({"telefone_fixo": fixo})
                
            
            celularAPI =getCelularAPI(response.text)                 
            if celularAPI is not None:
                celularAPI = celularAPI if celularAPI[:2] == '55' else None
                if celularAPI is not None:
                    session.query(Resultados).filter(Resultados.id == row.id).update({"telefone_celular": celularAPI })
            
            celular =getCelular(response.text) 
                                                      
            if celular is not None:
                session.query(Resultados).filter(Resultados.id == row.id).update({"telefone_celular": celular })
                
                
                
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

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):  
            # TODO: criar log ou armazenar no banco a url que der erro
            # continue
            break  
        
        
#TODO: Incluir arquivo .env com as configurações do banco etc
#TODO: limpar o codigo de forma funcionar como pacote