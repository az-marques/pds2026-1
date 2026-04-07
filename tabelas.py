from typing import Optional
from datetime import date
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.sql.expression import or_

class Base(DeclarativeBase):
    pass

class Individuo(Base):
    __tablename__ = "individuos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    sobrenome: Mapped[str] = mapped_column(String)

    parentesco_id: Mapped[Optional[int]] = mapped_column(ForeignKey("familias.id"))
    parentesco: Mapped[Optional["Familia"]] = relationship(back_populates="crianças")

    def nome_sobrenome(self):
        return f"{self.nome} {self.sobrenome}"
        
    def __repr__(self):
        return f"([{self.id}] {self.nome} {self.sobrenome})"


    
class Familia(Base):
    __tablename__ = "familias"
    id: Mapped[int] = mapped_column(primary_key=True)

    pais_id: Mapped[int] = mapped_column(ForeignKey("casamentos.id"))
    pais: Mapped["Casamento"] = relationship(back_populates="familia")

    crianças: Mapped[list["Individuo"]] = relationship(back_populates="parentesco")

    def __repr__(self):
        return f"Familia[{self.id}]\n  Pais=[{self.pais}]\n  Crianças={self.crianças}"
    

class Casamento(Base):
    __tablename__ = "casamentos"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[Optional[date]] = mapped_column()
    local: Mapped[Optional[str]] = mapped_column()

    conjuge_a_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    conjuge_a: Mapped["Individuo"] = relationship(foreign_keys=conjuge_a_id,
                                                   backref="casamentos_a")
    conjuge_b_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    conjuge_b: Mapped["Individuo"] = relationship(foreign_keys=conjuge_b_id,
                                                   backref="casamentos_b")

    familia: Mapped["Familia"] = relationship(back_populates="pais")

    def __repr__(self):
        return f"Casamento[{self.id}] ({self.conjuge_a_id}+{self.conjuge_b_id})"
    