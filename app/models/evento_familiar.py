from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Optional
from datetime import date
from .enums import FEvenTagEnum
from .base import Base

class EventoFamiliar(Base):
    __tablename__ = "eventos_familiares"
    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[FEvenTagEnum] = mapped_column(
        SQLEnum(FEvenTagEnum),
        nullable=False
    )
    
    data: Mapped[Optional[date]] = mapped_column()
    local: Mapped[Optional[str]] = mapped_column()
    notas: Mapped[Optional[str]] = mapped_column()

    fam_id: Mapped[int] = mapped_column(ForeignKey("familias.id"))
    fam: Mapped["Familia"] = relationship(back_populates="eventos")