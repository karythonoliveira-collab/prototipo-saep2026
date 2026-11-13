from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database.db import Base

class Item(Base):
    __tablename__ = "Item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    quantidade = Column(Float, nullable=False)
    validade = Column(String(50), nullable=True)
    cor = Column(String(45), nullable=True)
    unidade = Column(String(6), nullable=True)
  
    logs = relationship("Log", back_populates="item", cascade="all, delete-orphan")

    def __init__(self, quantidade=0.0):
        self.quantidade = quantidade