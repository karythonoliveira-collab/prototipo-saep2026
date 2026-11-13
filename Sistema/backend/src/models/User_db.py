from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base

class Usuario(Base):
    __tablename__ = "Usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(500), nullable=False)
    email = Column(String(500), nullable=False, unique=True)
    senha = Column(String(300), nullable=False)
    administrador = Column(Boolean, nullable=False)

    def __init__(self, admin=False):
        self.tipo = admin