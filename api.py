from resources import *
from flask import Flask,  request
from flask_restful import Resource, Api
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api = Api(app)


# item_pesquisa = cadastraPesquisa("abrasivos",1) #retorna id da pesquisa
# getDadosPesquisa(item_pesquisa) # processa as urls da pequisa informada com status pendente de processamento
# getDadosPesquisa(3) # coleta dados a partir de id_pesquisa
# coletaDadosUrl((185))  #Coleta dados informando um id e uma url da tabela resultados
# getDadosResultadoFalha(3) # processar Urls que deram falha a partir de id_pesquisa
# print(retornaPesquisas()) # retorna as pesquisa ja efetuadas
# print(retornaResultadosPesquisa(10)) # retorna resultados de uma pesquisa
# print(retornaDadosResultado(1)) #retorna dados do resultado


api.add_resource(DominiosIgnorados, '/dominios_ignorar/')
api.add_resource(DominiosIgnoradosRemove,
                 '/dominios_ignorar/<int:url_id>/')

api.add_resource(PesquisaList, '/termos_pesquisados/')
api.add_resource(Pesquisa, '/pesquisa/')
