from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import or_
from .base import Base
# from .individuo import Individuo
# from .casamento import Casamento

class Familia(Base):
    __tablename__ = "familias"
    id: Mapped[int] = mapped_column(primary_key=True)

    pais_id: Mapped[int] = mapped_column(ForeignKey("casamentos.id"))
    pais: Mapped["Casamento"] = relationship(back_populates="familia")

    crianças: Mapped[list["Individuo"]] = relationship(back_populates="parentesco")

    def __repr__(self):
        return f"Familia[{self.id}]\n  Pais=[{self.pais}]\n  Crianças={self.crianças}"