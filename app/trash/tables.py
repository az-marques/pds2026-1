from sqlalchemy import create_engine, Column, String, Integer

from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL="sqlite:///base_test_gene.db"

engine=create_engine(DATABASE_URL, echo=True)

Session=sessionmaker(bind=engine)

session=Session()

b = declarative_base()


# tabelas


b.metadata.create_all(bind=engine)