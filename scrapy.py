import urllib
from urllib.parse import urlparse, urlsplit
from bs4 import BeautifulSoup
from migrate import session,Pesquisa,PesquisaFalha,Resultados,PesquisaResultados,ResultadoCNPJ,ResultadoCEP,ResultadoTelefone,DominiosIgnorados,ResultadoEmail,ResultadoFalha
import util
import json
from collections import deque 
import numpy as np
from validate_email import validate_email

def getUrlGoogle(busca,item_pesquisa):
    busca = urllib.parse.quote_plus(busca)
    n_results = 3000

    url = "https://www.google.com/search?q=" + busca + "&num=" + str(n_results)
    
    try:
        response = util.getRequest(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        links = [a['href'] for a in soup.find_all('a', href=True)]
        for i in links:
            if i.startswith('https') or i.startswith('http'):
                ignorar = session.query(DominiosIgnorados).\
                    filter(DominiosIgnorados.dominio == urlparse(i).scheme+"://"+urlparse(i).netloc)\
                        .all() 
                if len(ignorar) == 0:
                    url = urlparse(i).scheme+"://"+urlparse(i).netloc
                    results.append(url)
        
        
        semDuplicados = np.unique(results).tolist()
        
        for i in semDuplicados:
            if i.find('blog') == -1: #removendo url de blog
                resultado = Resultados()
                resultado.url_base = i
                session.add(resultado)
                session.commit()

                pesquisa_resultado = PesquisaResultados()
                pesquisa_resultado.resultado_id =resultado.id
                pesquisa_resultado.pesquisa_id = item_pesquisa
                session.add(pesquisa_resultado)
        
        session.commit()
    except :
        falha = PesquisaFalha()
        falha.pesquisa_id = item_pesquisa
        falha.mensagem = util.getRequest(url)
    return (item_pesquisa)
    
    
def pesquisa(termo,usuario_id):
    
    item_pesquisa = Pesquisa()
    item_pesquisa.usuario_id = usuario_id
    item_pesquisa.termo = termo
    session.add(item_pesquisa)
    session.commit()
    
    
    
    
    pesquisa = getUrlGoogle(termo,item_pesquisa.id)
    getDados(pesquisa)

    
    # getDados(10)
    
    


    return "aui"




def getDados(item_pesquisa):

    VARRER_TODO_SITE =  False
    processed_urls = set() 
    emails = set()  

    result = session.query(Resultados)\
        .join(PesquisaResultados,Resultados.id == PesquisaResultados.resultado_id)\
        .filter(PesquisaResultados.pesquisa_id== item_pesquisa)\
        .filter(Resultados.status == 0)\
        .all()

    # result = session.query(Resultados)\
    #     .filter(Resultados.id > 33 )\
    #     .all()
        # 4 22
        # 61 125 113 145
        # .distinct()\
        # .filter(Resultados.cnpj == "" and Resultados.telefone_fixo == "" and Resultados.telefone_celular == "" and Resultados.cep == "")\
        # .filter(Resultados.dominio == 'www.cofermeta.com.br')\
        
    for row in result:
        
        new_urls = deque([row.url_base])
        while len(new_urls):  
            url = new_urls.popleft()  
            processed_urls.add(url)  

            # Defininado status para Pesquisando
            session.query(Resultados).\
                filter(Resultados.id == row.id).update({"status": 1})
            session.commit()
            response = util.getRequest(url)    

            # if response:
            try:
                parts = urlsplit(url)
                
                base_url = "{0.scheme}://{0.netloc}".format(parts)  
                path = url[:url.rfind('/')+1] if '/' in parts.path else url     
                
                getEmail(response.text,row.id)
                        
                getCNPJ(response.text,row.id)
          
                getCEP(response.text,row.id)
              
                getTelefone(response.text,row.id)
              
                # Atualizando status 
                session.query(Resultados).\
                    filter(Resultados.id == row.id).update({"status": 2})
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
                        if row.url_base == aux.netloc :
                            new_urls.append(link)  
            except:
                # Atualizando status 
                session.query(Resultados).\
                    filter(Resultados.id == row.id).update({"status": 3})
                
                falha = ResultadoFalha()
                falha.resultado_id = row.id
                falha.mensagem = str(response)
                session.add(falha)
                session.commit()
                continue
            
            

def getDadosCEP(cep):
    url = ('http://www.viacep.com.br/ws/%s/json' % cep)
    req = util.getRequest(url) 
    if req.status_code == 200:
        dados_json = json.loads(req.text)
        return dados_json


def getDadosCNPJ(cnpj):
    cnpj = util.parse_input(cnpj)
    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    req = util.getRequest(url)  
    if req.status_code == 200:
        return json.loads(req.text)

     
def getCNPJ(response,idResultado):
    cnpj = np.unique(util.regex('cnpj',response)).tolist()
    if len(cnpj):
        for i in cnpj:
            dadosCnpj =  getDadosCNPJ(util.parse_input(i))
            addCNPJ = ResultadoCNPJ()
            addCNPJ.resultado_id = idResultado
            addCNPJ.cnpj = util.parse_input(i).rjust(14, "0")
            addCNPJ.dados_cnpj = dadosCnpj
            addCNPJ.status= 1 if dadosCnpj['status'] == 'OK' else 2
            
            session.add(addCNPJ)
            session.commit()


def getCEP(response,idResultado):
    cep = np.unique([''.join(tups) for tups in util.regex('cep',response)]).tolist()
    if len(cep):
        for i in cep:
            dadosCep = getDadosCEP(util.parse_input(i))
            if not "erro" in dadosCep:
                addCep = ResultadoCEP()
                addCep.resultado_id = idResultado
                addCep.cep = i.rjust(8, "0") 
                addCep.dados_cep = dadosCep
                addCep.status = 1
                session.add(addCep)
                session.commit()


def getTelefone(response,idResultado):
    telefone = util.regex('telefone',response)
    telefone = [list(elem) for elem in telefone]
    telefone = np.unique([''.join(tups) for tups in telefone]).tolist()
    if len(telefone):
        for i in telefone:
            addTelefone = ResultadoTelefone()
            addTelefone.resultado_id = idResultado
            addTelefone.ddd = i[:2] if len(i) >=10  else None
            addTelefone.numero = i[2:]  if len(i) >=10 else i
           
            session.add(addTelefone)
            session.commit()
              
    # Caso possua alguma url de webwhatsapp, aqui armazena o numero
    telefoneAPI = util.regex('telefoneAPI',response)
    telefoneAPI = [list(elem) for elem in telefoneAPI]
    telefoneAPI = np.unique([''.join(tups) for tups in telefoneAPI]).tolist()

    if len(telefoneAPI):
        for i in telefoneAPI:
            addTelefone = ResultadoTelefone()
            addTelefone.resultado_id = idResultado
            addTelefone.numero = util.parse_input(i)
           
            session.add(addTelefone)
            session.commit()    
        
    
def getEmail(response,idResultado):
    email = np.unique(util.regex('email',response)).tolist()
    if len(email):
        for i in email:
            if validate_email(i,verify=True): #verifica se e-mail e valido
                addEmail = ResultadoEmail()
                addEmail.resultado_id = idResultado
                addEmail.email = i
                session.add(addEmail)
        session.commit()    

# Adicionar Url na tabela URL_IGNORAR
def addDominiosIgnorados(url):
    for i in url:    
        url_ignorar = DominiosIgnorados()
        url_ignorar.dominio = i if i[-1] != '/' else i[:-1]
        session.add(url_ignorar)
        session.commit()
    