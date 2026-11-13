from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Log(Base):
    __tablename__ = "Log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("Usuario.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("Item.id", ondelete="CASCADE"), nullable=False)
    dt = Column(String(50), nullable=False)
    quantidade = Column(Float, nullable=True, default=0.0)
    tipo = Column(String(7), nullable=False)

    usuario = relationship("Usuario")
    item = relationship("Item", back_populates="logs")
