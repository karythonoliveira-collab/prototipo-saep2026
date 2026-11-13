from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import relationship

from datetime import datetime

from ..db import Base

class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False, unique=True)
    preco_uni = Column(Numeric(10, 2), nullable=False)
    qtn = Column(Integer, nullable=False)
    dt_cads = Column(DateTime, nullable=False, default=datetime.now)

    logs = relationship("Log", back_populates="estoque")

    def __init__(self, nome: str, preco_uni: float, qtn: int, dt_cads: datetime =  datetime.now ) -> None:
        self.nome = nome
        self.preco_uni = preco_uni
        self.qtn = qtn
        self.dt_cads = dt_cads



