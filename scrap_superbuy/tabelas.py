from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
engine = create_engine('sqlite:///db_bot_superbuy.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


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
   endereco = Column(String)
   dados_cnpj = Column(String)


class UrlIgnorar(Base):
   __tablename__='url_ignorar'
   
   id = Column(Integer, primary_key=True)
   dominio = Column(String)    
       
   
Base.metadata.create_all(engine)