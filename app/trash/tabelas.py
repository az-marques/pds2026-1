import enum
from typing import Optional
from datetime import date
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.sql.expression import or_

class Base(DeclarativeBase):
    pass

class Gender(enum.Enum):
    M="masculino"
    F="feminino"
    NB="nao-binario"
    OTHER="outro" 
# class EventTag(enum.Enum):
#     BIRT = "Birth"
#     CHR = "Christening"
#     DEAT = "Death"
#     MARR = "Marriage"
#     DIV = "Divorce"
#     IMMI = "Immigration"
    
class EvenTagEnum(enum.Enum):
    BIRT = "Nascimento"
    CHR = "Batismo"
    DEAT = "Falecimento"
    MARR = "Casamento"
    IMMI = "Immigration"

class Individuo(Base):
    __tablename__ = "individuos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    sobrenome: Mapped[str] = mapped_column(String)
    # removido opcional para tornar genero obrigatorio/NOT NULL
    # substitui str por enum
    # outro: padrao caso nao informado
    genero: Mapped[Gender] = mapped_column(default=Gender.OTHER)
    
    # boolean vivo True or False
    vivo: Mapped[bool] = mapped_column(default=True)
    
    parentesco_id: Mapped[Optional[int]] = mapped_column(ForeignKey("familias.id"))
    parentesco: Mapped[Optional["Familia"]] = relationship(back_populates="crianças")

    eventos: Mapped[Optional[list["Evento"]]] = relationship(back_populates="indi")

    # def nome_sobrenome(self):
    #     return f"{self.nome} {self.sobrenome}"
    # def __repr__(self):
    #     return f"([{self.id}] {self.nome} {self.sobrenome})"
    
    def __repr__(self) -> str:
        status = "Vivo" if self.vivo else "Falecido"
        return f"([{self.id}] {self.nome} {self.sobrenome} - {self.genero} - {status})"

class Familia(Base):
    __tablename__ = "familias"
    id: Mapped[int] = mapped_column(primary_key=True)

    pais_id: Mapped[int] = mapped_column(ForeignKey("casamentos.id"))
    pais: Mapped["Casamento"] = relationship(back_populates="familia")

    crianças: Mapped[list["Individuo"]] = relationship(back_populates="parentesco")

    def __repr__(self):
        return f"Familia[{self.id}]\n  Pais=[{self.pais}]\n  Crianças={self.crianças}"
    
class Local(Base):
    __tablename__="locais"
    id: Mapped[int]=mapped_column(primary_key=True)
    
    # Detalhes geográficos normalizados
    cidade: Mapped[Optional[str]] = mapped_column(String)
    estado: Mapped[Optional[str]] = mapped_column(String) # Opcional (ex: países sem estados)
    pais: Mapped[str] = mapped_column(String)
    regiao: Mapped[Optional[str]] = mapped_column(String) # Ex: Europa, América do Sul, etc.
    
    #resolver regiao
    def __repr__(self) -> str:
        
        loc_str_formatado = f"id=[{self.id}] "
        
        if not self.regiao:
            self.regiao="null"
            
        if not self.cidade:
            self.cidade="null"
            
        if not self.estado:
            self.estado="null"
            
        loc_str_formatado = loc_str_formatado + f"{self.cidade}, {self.estado}, {self.pais}"
            
        return (loc_str_formatado)
# def nome_formatado(self) -> str:
#         partes = [self.cidade]
#         if self.estado: partes.append(self.estado)
#         partes.append(self.pais)
#         return ", ".join(partes)


class Casamento(Base):
    __tablename__ = "casamentos"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    dia_casamento: Mapped[Optional[int]]=mapped_column()
    mes_casamento: Mapped[Optional[int]]=mapped_column()
    ano_casamento: Mapped[Optional[int]]=mapped_column()
    
    #local: Mapped[Optional[str]] = mapped_column() local vem de outra tabela
    
    

    conjuge_a_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    conjuge_a: Mapped["Individuo"] = relationship(foreign_keys=conjuge_a_id,
                                                   backref="casamentos_a")
    conjuge_b_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    conjuge_b: Mapped["Individuo"] = relationship(foreign_keys=conjuge_b_id,
                                                   backref="casamentos_b")

    familia: Mapped["Familia"] = relationship(back_populates="pais")

    def __repr__(self):
        return f"Casamento[{self.id}] ({self.conjuge_a_id}+{self.conjuge_b_id})"

class Evento(Base):
    __tablename__ = "eventos"
    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[EvenTagEnum] = mapped_column(
        SQLEnum(EvenTagEnum),
        nullable=False
    )
    
    # data: dia INT, mes IND -> opcionais
    dia: Mapped[Optional[int]]=mapped_column()
    mes: Mapped[Optional[int]]=mapped_column()
    
    # data.ano: obrigatorio
    ano: Mapped[int]=mapped_column(nullable=False)
    
    data_exata: Mapped[bool] = mapped_column(default=True)
    
    # data: Mapped[Optional[date]] = mapped_column()
    # local: Mapped[Optional[str]] = mapped_column()
    notas: Mapped[Optional[str]] = mapped_column()

    indi_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    indi: Mapped["Individuo"] = relationship(back_populates="eventos")
    
    def get_ev_indi(self) -> tuple:
        
        fullname=self.indi.nome_sobrenome() if self.indi else "Indi desconhecido"
        
        return (
            self.self.tag.value,
            self.dia,
            self.mes,
            self.ano,
            self.notas,
            fullname
        )


# class Evento(Base):
#     __tablename__ = "eventos"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     # tipo: Mapped[str] = mapped_column()
    
#     tag: Mapped[EvenTagEnum] = mapped_column()
#     data: Mapped[Optional[date]] = mapped_column()
#     local: Mapped[Optional[str]] = mapped_column()
#     notas: Mapped[Optional[str]] = mapped_column()

#     indi_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
#     indi: Mapped["Individuo"] = relationship(back_populates="eventos")    
    
