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
    try:
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
    except:
        pass

def getCEP(response,idResultado):
    try:
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
    except:
        pass

def getTelefone(response,idResultado):
    try:
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
    except:
        pass        
    
def getEmail(response,idResultado):
    try:
        email = np.unique(util.regex('email',response)).tolist()
        if len(email):
            for i in email:
                if validate_email(i,verify=True): #verifica se e-mail e valido
                    addEmail = ResultadoEmail()
                    addEmail.resultado_id = idResultado
                    addEmail.email = i
                    session.add(addEmail)
            session.commit()    
    except:
        pass

# Adicionar Url na tabela URL_IGNORAR
def addDominiosIgnorados(url):
    for i in url:    
        url_ignorar = DominiosIgnorados()
        url_ignorar.dominio = i if i[-1] != '/' else i[:-1]
        session.add(url_ignorar)
        session.commit()

def coletaDadosUrl(id_url,url_base=False):

    session.query(Resultados).\
        filter(Resultados.id == id_url).update({"status": 1})
        
    if not url_base:
        row = session.query(Resultados).\
                filter(Resultados.id == id_url).one()
        url_base = row.url_base
        id_url = row.id
    # import pdb; pdb.set_trace()
    response = util.getRequest(url_base)    

    try:
        getEmail(response.text,id_url)
        getCNPJ(response.text,id_url)
        getCEP(response.text,id_url)
        getTelefone(response.text,id_url)
        
        # Atualizando status 
        session.query(Resultados).\
            filter(Resultados.id == id_url).update({"status": 2})
        session.commit()
        
    except:
        session.query(Resultados).\
            filter(Resultados.id == id_url).update({"status": 3})
        
        falha = ResultadoFalha()
        falha.resultado_id = id_url
        falha.mensagem = str(response)
        session.add(falha)
        session.commit()
            
def getDadosPesquisa(item_pesquisa):
    
    result = session.query(Resultados)\
        .join(PesquisaResultados,Resultados.id == PesquisaResultados.resultado_id)\
        .filter(PesquisaResultados.pesquisa_id== item_pesquisa)\
        .filter(Resultados.status == 0)\
        .all()

    for i in result:
        coletaDadosUrl(i.id,i.url_base)    

def getDadosResultadoFalha(item_pesquisa):

    result = session.query(Resultados).\
            join(PesquisaResultados,PesquisaResultados.resultado_id == Resultados.id).\
            join(ResultadoFalha,ResultadoFalha.resultado_id == Resultados.id).\
            filter(PesquisaResultados.pesquisa_id == item_pesquisa).\
            all()
    for i in result:
        # remove da tabela de falhas o registro que sera reprocessado
        session.query(ResultadoFalha).filter(ResultadoFalha.resultado_id == i.id).delete()
        coletaDadosUrl(i.id,i.url_base)    
    
def cadastraPesquisa(termo,usuario_id):

    # item_pesquisa = Pesquisa()
    # item_pesquisa.usuario_id = usuario_id
    # item_pesquisa.termo = termo
    # session.add(item_pesquisa)
    # session.commit()#todo: incluir try para tabela de pesquisa_erro
         
    # pesquisa = getUrlGoogle(termo,item_pesquisa.id)
    # getDadosPesquisa(pesquisa)
    
    # getDadosPesquisa(3) # coleta dados a partir de id_pesquisa
    # coletaDadosUrl((185))  Coleta dados informando um id e uma url da tabela resultados
    # getDadosResultadoFalha(3) # processar Urls que deram falha a partir de id_pesquisa

    print(retornaPesquisas()) # retorna dados da pesquisa
    return "Processado"

def retornaPesquisas():
    result = session.query(Pesquisa).\
            all()
    
    for i in result:
        import pdb; pdb.set_trace()


    import pdb; pdb.set_trace()
    def create_item(item):
        return {
            'id':item.id,
            'termo':item.termo,
            'status':item.status,
            'data_pesquisa':item.data_pesquisa,
            
        }
    
    
    return json.dumps({u'results': map(create_item,result)})
   