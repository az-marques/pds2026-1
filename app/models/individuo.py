# APAGUE ESTAS LINHAS:
# from .evento import Evento
# from .familia import Familia
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from .enums import GenderEnum
from .base import Base

class Individuo(Base):
    __tablename__ = "individuos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    sobrenome: Mapped[str] = mapped_column(String)
    # removido opcional para tornar genero obrigatorio/NOT NULL
    # substitui str por enum
    # outro: padrao caso nao informado
    genero: Mapped[GenderEnum] = mapped_column(
        SQLEnum(GenderEnum), 
        nullable=False,
        default=GenderEnum.OTHER) # opcional = native_enum=False
    
    parentesco_id: Mapped[Optional[int]] = mapped_column(ForeignKey("familias.id"))
    parentesco: Mapped[Optional["Familia"]] = relationship(back_populates="crianças")

    eventos: Mapped[Optional[list["Evento"]]] = relationship(back_populates="indi")
    
    def nome_sobrenome(self):
         return f"{self.nome} {self.sobrenome}"
    
    def __repr__(self) -> str:
        return f"([{self.id}] {self.nome} {self.sobrenome} - {self.genero})"