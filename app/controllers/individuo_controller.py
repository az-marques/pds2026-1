# importacoes de controle de individuo
# sqlalchemy orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
# validacao com pydantic
from pydantic import BaseModel, Field, field_validator, ValidationError
# tabelas.py -> models
from app.models.tabelas import Individuo

from datetime import date
import re
# db -> controller
# main -> GUI.py
class IndividuoSchema(BaseModel):
    
    nome: str=Field(..., min_length=2, max_length=100, description="Primeiro nome da pessoa")
    sobrenome: str=Field(..., min_length=2, max_length=100, description="Sobrenome da pessoa")
    # genero
    # data_nasc: date | None = None
    # local_nasc: str | None = Field(default=None, max_length=100)
    # notas: str | None = Field(default=None, max_length=100)
    # DT/LOC NASC
    
    @field_validator("nome", "sobrenome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", valor):
            raise ValueError("Nome deve conter apenas letras")
        return valor.strip()


class IndividuoController:
    def __init__(self, session_maker: sessionmaker):
        # injeta a fabrica de sessoes do sqlalchemy
        # permite usar psql ou sqlite
        self.Session = session_maker
        
    def cria_individuo(self, dados_entrada: dict):
        # 1-pydantic
        # recebe um dicionario
        try:
            # valida com o esquema do pydantic
            dados_validados=IndividuoSchema(**dados_entrada)
        except ValidationError as e:
            # erro capturado pelo pydantic
            raise ValueError(f"Erro de Validação:\n{e.errors()[0]['msg']}")
        
        # 2-transacao com a base de dados
        with self.Session() as session:
            try:
                novo_indi=Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome
                )
                session.add(novo_indi)
                session.commit()
                session.refresh(novo_indi)
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}")
            

    # def _validar_nome(self, texto: str, nome_campo: str) -> str:
    #     """
    #     Validação de Back-end (Segurança e Integridade).
    #     Garante que não passam números ou símbolos, mesmo que a UI falhe.
    #     """
    #     if not texto or not texto.strip():
    #         raise ValueError(f"O {nome_campo} é obrigatório.")
            
    #     texto = texto.strip()
    #     # Regex: Permite letras (incluindo acentos) e espaços
    #     if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", texto):
    #         raise ValueError(f"O {nome_campo} contém caracteres inválidos (números ou símbolos).")
            
    #     return texto
    
    
    # def adicionar_individuo(self, nome: str, sobrenome: str, genero: str, dtnasc: str, loc_nasc: str):
        
        
    #     return

# data = PersonCreate(**input_data)

# person = Person(
#     full_name=data.full_name,
#     birth_date=data.birth_date,
# )