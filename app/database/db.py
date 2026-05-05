from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base
# from app.models import *
# URL do banco de dados (pode ser movida para um .env futuramente)
DATABASE_URL = "sqlite:///base_test_gene.db"

# cria o motor de conexao
engine = create_engine(DATABASE_URL, echo=True)

# cria a fabrica de sessoes usada pelo controller
Session = sessionmaker(bind=engine)

def init_db():
    # cria todas as tabelas do banco de dados se elas ainda nao existirem
    Base.metadata.create_all(bind=engine)