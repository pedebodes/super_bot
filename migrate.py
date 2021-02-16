
import os
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import Column, Integer, String, JSON,ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

load_dotenv(find_dotenv())
Base = declarative_base()

engine = create_engine(os.environ.get("DATABASE_URL"), echo=bool(os.environ.get("ECHO")))

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
class UrlBase(Base):
    __tablename__='url_base'    
    id = Column(Integer, primary_key=True)
    dominio = Column(String)    
    url =Column(String) 
    cnpj = Column(String)
    telefone_fixo = Column(String)
    telefone_celular = Column(String)
    cep = Column(String)
    email = Column(String)
    endereco = Column(JSON)
    dados_cnpj = Column(JSON)
    

class ItemPesquisa(Base):
    __tablename__='item_pesquisa'
    id = Column(Integer, primary_key=True)
    item = Column(String)    


class itemUrl(Base):
    __tablename__ = 'item_url'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('url_base.id'), nullable=True)
    item_pesquisa_id = Column(Integer, ForeignKey('item_pesquisa.id'), nullable=True)
    
    urlBase = relationship(UrlBase, backref=backref("item_url"))
    item = relationship(ItemPesquisa, backref=backref("item_url"))
        

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
