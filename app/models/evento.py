from sqlalchemy import ForeignKey, select, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import or_

from typing import Optional
from datetime import date
from .enums import EvenTagEnum
from .base import Base
# from .individuo import Individuo

class Evento(Base):
    __tablename__ = "eventos"
    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[EvenTagEnum] = mapped_column(
        SQLEnum(EvenTagEnum),
        nullable=False
    )
    
    data: Mapped[Optional[date]] = mapped_column()
    local: Mapped[Optional[str]] = mapped_column()
    notas: Mapped[Optional[str]] = mapped_column()

    indi_id: Mapped[int] = mapped_column(ForeignKey("individuos.id"))
    indi: Mapped["Individuo"] = relationship(back_populates="eventos")