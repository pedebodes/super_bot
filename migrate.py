
import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
load_dotenv(find_dotenv())
Base = declarative_base()


engine = create_engine(os.environ.get("DATABASE_URL"), echo=True)

class UrlBase(Base):
    __tablename__='url_base'    
    # TODO: pendente correção dos campos 
    id = Column(Integer, primary_key=True)
    dominio = Column(String)    
    url =Column(String) 
    cnpj = Column(String)
    telefone_fixo = Column(String)
    telefone_celular = Column(String)
    cep = Column(String)
    email = Column(String)
    endereco = Column(String)
    dados_cnpj = Column(String)
    complementar = Column(JSON) ############# REMOVER

class UrlIgnorar(Base):
    __tablename__='url_ignorar'
    id = Column(Integer, primary_key=True)
    dominio = Column(String)    


def create_tables():
    try:
        Base.metadata.create_all(engine)
        print ("Executado com sucesso.")
    except:
        print ("Ocorreu erro na criação das tabelas, favor verificar")


def main():
    create_tables()
    

if __name__=='__main__':
    main()
