from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from argon2 import PasswordHasher

from ..db.conection import Base


ph = PasswordHasher()


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    nome = Column(String(120), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=0)

    logs = relationship("Log", back_populates="usuario")

    def __init__(self, email: str, senha: str, nome: str, is_admin: bool = False) -> None:
        self.email = email
        self.senha = ph.hash(senha)
        self.nome = nome
        self.is_admin = int(is_admin)

    def nova_senha(self, nova_senha:str) -> None:
        self.senha = ph.hash(nova_senha)

    def verificar_senha(self, senha: str) -> bool:
        return ph.verify(hash=self.senha, password=senha)

    