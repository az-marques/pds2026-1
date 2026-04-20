import enum
from typing import Optional
from datetime import date
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.sql.expression import or_
from .base import Base
# from .individuo import Individuo
# from .familia import Familia

class Casamento(Base):
    __tablename__ = "casamentos"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[Optional[date]] = mapped_column()
    local: Mapped[Optional[str]] = mapped_column()
    notas: Mapped[Optional[str]] = mapped_column()

    conjuge_a_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    conjuge_a: Mapped["Individuo"] = relationship(foreign_keys=conjuge_a_id,
                                                   backref="casamentos_a")
    conjuge_b_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    conjuge_b: Mapped["Individuo"] = relationship(foreign_keys=conjuge_b_id,
                                                   backref="casamentos_b")

    familia: Mapped["Familia"] = relationship(back_populates="pais")

    def __repr__(self):
        return f"Casamento[{self.id}] ({self.conjuge_a_id}+{self.conjuge_b_id})"