from flask import Flask,  request
from flask_restful import Resource, Api
from flask_cors import CORS

import scrapy

app = Flask(__name__)
CORS(app)
api = Api(app)


class DominiosIgnorados(Resource):
    def post(self):
        try:
            dados = request.get_json()
            x = scrapy.addDominiosIgnorados(dados['url'])
            return {'success': "Cadastro realizado"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    def get(self):
        try:
            return {'success': scrapy.getDominiosIgnorados()}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class DominiosIgnoradosRemove(Resource):
    def delete(self, url_id):
        try:
            scrapy.delDominiosIgnorados(url_id)
            return {'success': "Url removida"}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class Resultado(Resource):
    def get(self, pesquisa_id):
        try:
            return {'success': scrapy.retornaResultadosPesquisa(pesquisa_id)}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class Pesquisa(Resource):
    def post(self):
        try:
            dados = request.get_json()
            item_pesquisa = scrapy.cadastraPesquisa(dados['termo'], dados['user_id'])

            if item_pesquisa['status'] == "cadastrado com sucesso":
                scrapy.getPesquisa(dados['termo'], item_pesquisa['item_pesquisa'])
           
            return {'success': {"status": item_pesquisa['status'],
                                "itemPesquisa": item_pesquisa}}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    def get(self):
        try:
            return {'success': scrapy.retornaPesquisas()}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class DadosUrl(Resource):
    def post(self):
        dados = request.get_json()

        scrapy.coletaDadosUrl(dados['url_id'])
        return {'success': "coletado"}, 200


class DadosTermo(Resource):
    def post(self):
        dados = request.get_json()

        scrapy.getDadosPesquisa(dados['termo_id'])
        return {'success': "coletado"}, 200


class ReprocessaPesquisaFalha(Resource):
    def get(sel, termo_id):
        scrapy.getDadosResultadoFalha(termo_id)
        return {'success': "reprocessado"}, 200

    
api.add_resource(DominiosIgnorados, '/dominios_ignorar/')
api.add_resource(DominiosIgnoradosRemove, '/dominios_ignorar/<int:url_id>/')
api.add_resource(Pesquisa, '/pesquisa/')
api.add_resource(Resultado, '/resultado/<int:pesquisa_id>')
api.add_resource(DadosUrl, '/coletar_dados_url/')
api.add_resource(DadosTermo, '/coletar_dados_termo/')
api.add_resource(ReprocessaPesquisaFalha,'/reprocessa_pesquisa_falha/<int:termo_id>/')
