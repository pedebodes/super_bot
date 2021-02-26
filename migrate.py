
import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import Column, Integer, String,ForeignKey,DateTime,CHAR
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker,mapper
import datetime

from sqlalchemy.sql.expression import column
# from citext import CIText # ERRO NO POSTGRES: type "citext" does not exist
load_dotenv(find_dotenv())
Base = declarative_base()

engine = create_engine(os.environ.get("DATABASE_URL"), echo=bool(os.environ.get("ECHO")))

Session = sessionmaker(bind = engine)
session = Session()

class Pesquisa(Base):
    __tablename__='pesquisas'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)
    termo = Column(String)
    status = Column(Integer, default=0)
    data_pesquisa = Column(DateTime, default=datetime.datetime.now())  

    # Status
    # 0 = pendente de execucao
    # 1 = em execucao?
    # 2 = concluida com sucesso
    # 3 = concluida com falha

class PesquisaFalha(Base):
    __tablename__='pesquisa_falhas'
    id = Column(Integer, primary_key=True)
    pesquisa_id = Column(Integer, ForeignKey('pesquisas.id'), nullable=True)
    mensagem = Column(String)
    
    id_pesquisa = relationship(Pesquisa, backref=backref("pesquisa_falhas"))

class Resultados(Base):
    __tablename__='resultados'
    id = Column(Integer, primary_key=True)
    url_base = Column(String)
    status = Column(Integer,default=0)
    # status
    #     0 = pendente de detalhes
    #     1 = em execucao?
    #     2 = concluida com sucesso
    #     3 = concluida com falha    

class ResultadoFalha(Base):
    __tablename__='resultado_falhas'
    id = Column(Integer, primary_key=True)
    resultado_id = Column(Integer, ForeignKey('resultados.id'), nullable=True)
    mensagem = Column(String)
    
    id_resultado = relationship(Resultados, backref=backref("resultado_falhas"))
class PesquisaResultados(Base):
    __tablename__='pesquisa_resultados'
    id = Column(Integer, primary_key=True)
    pesquisa_id = Column(Integer, ForeignKey('pesquisas.id'), nullable=True)
    resultado_id = Column(Integer, ForeignKey('resultados.id'), nullable=True)
    
    id_pesquisa = relationship(Pesquisa, backref=backref("pesquisa_resultados"))
    id_resultado = relationship(Resultados, backref=backref("pesquisa_resultados"))
    
    
class ResultadoCNPJ(Base):
    __tablename__='resultados_cnpj'
    id = Column(Integer, primary_key=True)
    resultado_id = Column(Integer, ForeignKey('resultados.id'), nullable=True)
    cnpj = Column(String(14))
    dados_cnpj = Column(JSONB)
    status = Column(Integer, default=0)
    
    id_resultado = relationship(Resultados, backref=backref("resultados_cnpj"))
    # Status:
    # 0 - pendente
    # 1 - executado
    # 2 - falha na execução
    
class ResultadoCEP(Base):
    __tablename__='resultados_cep'
    id = Column(Integer, primary_key=True)
    resultado_id = Column(Integer, ForeignKey('resultados.id'), nullable=True)
    cep = Column(String(8)) 
    dados_cep = Column(JSONB) 
    status = Column(Integer, default=0)
    
    id_resultado = relationship(Resultados, backref=backref("resultados_cep"))
    # Status:
    # 0 - pendente
    # 1 - executado
    # 2 - falha na execução
    
    
class ResultadoTelefone(Base):
    __tablename__='resultados_telefone'
    id = Column(Integer, primary_key=True)
    resultado_id = Column(Integer, ForeignKey('resultados.id'), nullable=True)
    ddd = Column(CHAR(2))
    numero = Column(CHAR(13))
    status = Column(Integer, default=0)
    
    id_resultado = relationship(Resultados, backref=backref("resultados_telefone"))
    #Status:
    # 0 - Não avaliado
    # 1 - Valido
    # 2 - Invalido
    
    
    
    
status_bosta = {
  0: u'Não avaliado',
  1: u'Valido',
  2: u'Invalido'
}    
class ResultadoEmail(Base):
    __tablename__='resultados_email'
    id = Column(Integer, primary_key=True)
    resultado_id = Column(Integer, ForeignKey('resultados.id'), nullable=True)
    email = Column(String)
    status = Column(Integer, default=0)
    
    id_resultado = relationship(Resultados, backref=backref("resultados_email"))
    #Status:
    # 0 - Não avaliado
    # 1 - Valido
    # 2 - Invalido



class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    discriminator = Column(String(50))


    @property
    def tipo_descricao(self):
        try:
            s = status_bosta[self.tipo]
        except KeyError:
            s = u'Tipo desconhecido'
        return s


  











    
class DominiosIgnorados(Base):
    __tablename__='dominios_ignorar'
    id = Column(Integer, primary_key=True)
    dominio = Column(String)    


def create_tables():
    try:
        Base.metadata.create_all(engine)
        print ("Executado com sucesso.")
    except:
        print ("Ocorreu erro na criação das tabelas, favor verificar")


def main():
    Base.metadata.create_all(engine)

    create_tables()
    

if __name__=='__main__':
    main()
