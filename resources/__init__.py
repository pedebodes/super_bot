from flask_restful import Resource
from flask import request
import scrapy


class DominiosIgnorados(Resource):
    def post(self):
        try:
            dados = request.get_json()
            x = scrapy.addDominiosIgnorados(dados['url'])
            return {'sucess': "Cadastro realizado"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    def get(self):
        try:
            return {'sucess': scrapy.getDominiosIgnorados()}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class DominiosIgnoradosRemove(Resource):
    def delete(self, url_id):
        try:
            scrapy.delDominiosIgnorados(url_id)
            return {'sucess': "Url removida"}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class PesquisaList(Resource):
    def get(self):
        try:
            return {'sucess': scrapy.retornaPesquisas()}, 200
        except Exception as e:
            return {"error": str(e)}, 400


class Pesquisa(Resource):
    def post(self):
        try:
            dados = request.get_json()
            item_pesquisa = scrapy.cadastraPesquisa(
                dados['termo'], dados['user_id'])
            if item_pesquisa['status'] == 'cadastrado com sucesso':
                scrapy.getPesquisa(
                    dados['termo'], item_pesquisa['item_pesquisa'])
            return {'sucess': {"status": item_pesquisa['status'],
                               "itemPesquisa": item_pesquisa}}, 200
        except Exception as e:
            return {"error": str(e)}, 400
