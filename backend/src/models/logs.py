from sqlalchemy import Column, DATETIME, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db import Base

class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_estoque = Column(Integer, ForeignKey("estoque.id", ondelete="CASCADE"), primary_key=True, nullable=False,)
    dt_acao = Column(DATETIME, nullable=False, default=datetime.now())
    is_retirada = Column(Boolean, nullable=False, default=0)

    usuario = relationship("Usuario", back_populates="logs")
    estoque = relationship("Estoque", back_populates="logs")

    def __init__(self, id_usuario: int, id_estoque: int, qtn_acao: int, dt_acao: datetime = datetime.now(), is_retirada: bool = False):
        self.id_usuario = id_usuario
        self.id_estoque = id_estoque
        self.qtn_acao = qtn_acao
        self.dt_acao = dt_acao
        self.is_retirada = int(is_retirada)
