from flask_restful import Resource
from flask import request
import scrapy


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
    def get(self,pesquisa_id):
        try:
            return {'success': scrapy.retornaResultadosPesquisa(pesquisa_id)}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class Pesquisa(Resource):
    def post(self):
        try:
            dados = request.get_json()
            item_pesquisa = scrapy.cadastraPesquisa(
                dados['termo'], dados['user_id'])
            if item_pesquisa['status'] == 'cadastrado com successo':
                scrapy.getPesquisa(
                    dados['termo'], item_pesquisa['item_pesquisa'])
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
