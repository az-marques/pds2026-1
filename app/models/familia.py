from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import or_
from .base import Base
# from .individuo import Individuo
# from .casamento import Casamento

class Familia(Base):
    __tablename__ = "familias"
    id: Mapped[int] = mapped_column(primary_key=True)

    #pais_id: Mapped[int] = mapped_column(ForeignKey("casamentos.id"))
    #pais: Mapped["Casamento"] = relationship(back_populates="familia")

    pai_a_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    pai_a: Mapped["Individuo"] = relationship(foreign_keys=pai_a_id,
                                                   backref="casamentos_a")
    pai_b_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    pai_b: Mapped["Individuo"] = relationship(foreign_keys=pai_b_id,
                                                   backref="casamentos_b")

    #crianças: Mapped[list["Individuo"]] = relationship(back_populates="parentesco", foreign_keys="individuos.parentesco_id")

    def __repr__(self):
        return f"Familia[{self.id}]\n  Pais=[{self.pai_a_id}] [{self.pai_b_id}]\n  Crianças={self.crianças}"