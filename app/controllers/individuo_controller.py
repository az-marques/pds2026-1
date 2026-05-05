# importacoes de controle de individuo
# sqlalchemy orm
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
# validacao com pydantic
from pydantic import BaseModel, Field, field_validator, ValidationError
# tabelas.py -> models

from app.models.individuo import Individuo
from app.models.evento import Evento
from app.models.evento_familiar import EventoFamiliar
from app.models.familia import Familia
from app.models.enums import GenderEnum, EvenTagEnum, FEvenTagEnum

from datetime import date
import re
# db -> controller
# main -> GUI.py

class EventSchema(BaseModel):
    tag: EvenTagEnum
    data: date
    local: str=Field(..., min_length=2, max_length=100, description="Local do evento")
    notas: Optional[str] = None # nao precisa de uma mascara?
    # @field_validator("death_date")
    # def validate_dates(cls, value, info):
    #     birth = info.data.get("birth_date")

    #     if value and birth and value < birth:
    #         raise ValueError("Data de morte não pode ser antes do nascimento")

    #     return value

class FamilyEventSchema(BaseModel):
    tag: FEvenTagEnum
    data: date
    local: str=Field(..., min_length=2, max_length=100, description="Local do evento")
    notas: Optional[str] = None # nao precisa de uma mascara?

class IndividuoSchema(BaseModel):
    nome: str=Field(..., min_length=2, max_length=50, description="Primeiro nome da pessoa")
    sobrenome: str=Field(..., min_length=2, max_length=50, description="Sobrenome da pessoa")
    # validacao suja, nao sei como validar isso, mas tbm nao acho necessario
    genero: GenderEnum
    
    @field_validator("nome", "sobrenome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        
        # if not valor:
        #     raise ValueError("O campo nao pode estar vazio")
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", valor):
            raise ValueError("Nome deve conter apenas letras")
        return valor.strip()

class IndividuoController:
    def __init__(self, ses_mkr: sessionmaker):
        # injeta a fabrica de sessoes do sqlalchemy
        # permite usar psql ou sqlite
        self.Session = ses_mkr
        
    def cria_individuo(self, dados_entrada: dict):
        # 1-pydantic
        # recebe um dicionario
        eventos=[] # cria uma lista vazia de eventos da pessoa
        try:
            # valida com o esquema do pydantic
            dados_validados=IndividuoSchema(**dados_entrada) # ** serve para desencapsular dicionario
            nascimento=EventSchema(**dados_entrada["nascimento"])
            eventos.append(nascimento)
            
            # validar dados
        except ValidationError as err:
            # erro capturado pelo pydantic
            raise ValueError(f"Erro de Validação:\n{err.errors()[0]['msg']}")
        
        # 2-transacao com a base de dados
        with self.Session() as session:
            try:
                # cria o individuo com seus dados pessoais
                novo_indi = Individuo(
                    nome=dados_validados.nome,
                    sobrenome=dados_validados.sobrenome,
                    genero=dados_validados.genero,
                )
                session.add(novo_indi)
                session.flush() # garante que indi esta disponivel
                
                for evento in eventos:
                    novo_event=Evento(
                        tag=EvenTagEnum.BIRT, # logica errada
                        data=evento.data,
                        local=evento.local.strip(),
                        notas=evento.notas,
                        indi_id=novo_indi.id
                    )
                    session.add(novo_event)

                # novo_indi.eventos.append(eventonascimento)
                session.commit()
                session.refresh(novo_indi)
                
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}")

    #retorna um dicionário com os dados do indivíduo
    def acessa_individuo(self, indi_id: int) -> dict:
        with self.Session() as session:
            try:
                stmt = select(Individuo).where(Individuo.id == indi_id)
                resultado = session.scalars(stmt).one()

                dados = {
                    "id": resultado.id,
                    "nome": resultado.nome,
                    "sobrenome": resultado.nome,
                    "genero": resultado.genero,
                    "parentesco_id": resultado.parentesco.id
                }
                return dados
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}")
    
    def cria_familia(self, pai_a_id: int, pai_b_id: int, dados_casamento: Optional[dict]):
        if dados_casamento:
            try:
                dados_casamento["tag"] = FEvenTagEnum.MARR
                # valida com o esquema do pydantic
                dados_validados=FamilyEventSchema(**dados_casamento) # ** serve para desencapsular dicionario
            except ValidationError as err:
                # erro capturado pelo pydantic
                raise ValueError(f"Erro de Validação:\n{err.errors()[0]['msg']}")

        #transação com a DB
        with self.Session() as session:
            try:
                nova_familia = Familia(
                    pai_a_id=pai_a_id,
                    pai_b_id=pai_b_id
                )

                if (dados_casamento):
                    casamento = EventoFamiliar(
                        tag=dados_validados.tag,
                        data=dados_validados.data,
                        local=dados_validados.local,
                        notas=dados_validados.notas
                    )
                    nova_familia.eventos.append(casamento)
                


                session.add(nova_familia)
                session.flush()
                session.commit()
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}")

    def cria_evento_individual(self, indi_id: int, dados_evento: dict):
        # 1-pydantic
        # recebe um dicionario
        try:
            # valida com o esquema do pydantic
            dados_validados=EventSchema(**dados_evento) # ** serve para desencapsular dicionario
        except ValidationError as err:
            # erro capturado pelo pydantic
            raise ValueError(f"Erro de Validação:\n{err.errors()[0]['msg']}")

        # 2-transacao com a base de dados
        with self.Session() as session:
            try:
                novo_evento = Evento(
                    indi_id=indi_id, #adicionar verificão de que o indivíduo existe de algum jeito?
                    tag=dados_validados.tag,
                    data=dados_validados.data,
                    local=dados_validados.local,
                    notas=dados_validados.notas
                )

                session.add(novo_evento)
                session.flush()
                session.commit()
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}")
            
    def cria_evento_familiar(self, fam_id: int, dados_evento: dict):
        # 1-pydantic
        # recebe um dicionario
        try:
            # valida com o esquema do pydantic
            dados_validados=FamilyEventSchema(**dados_evento) # ** serve para desencapsular dicionario
        except ValidationError as err:
            # erro capturado pelo pydantic
            raise ValueError(f"Erro de Validação:\n{err.errors()[0]['msg']}")

        # 2-transacao com a base de dados
        with self.Session() as session:
            try:
                novo_evento = EventoFamiliar(
                    fam_id=fam_id, #adicionar verificão de que a família existe de algum jeito?
                    tag=dados_validados.tag,
                    data=dados_validados.data,
                    local=dados_validados.local,
                    notas=dados_validados.notas
                )

                session.add(novo_evento)
                session.flush()
                session.commit()
            except SQLAlchemyError as err_db:
                session.rollback()
                raise Exception(f"Erro na base de dados: {str(err_db)}")
