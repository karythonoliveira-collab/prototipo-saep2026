from click import DateTime
from psycopg import Date
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Numeric, String, null
from decimal import Decimal
from sqlalchemy.orm import relationship
from datetime import date, datetime

from torch import R
from database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id_user = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    perfil = Column(String(50), nullable=False, default="operador")

    movimentacoes = relationship("MovimentacaoModel", back_populates="usuarios")

class ProdutoModel(Base):

    __tablename__ = "produto"
    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    quantidade_estoque = Column(Integer, nullable=False)
    valor_uni = Column(Integer, nullable=False)
    data_cadastro = Column(Date, nullable=False, default=date.today)
    movimentacoes = relationship("MovimentacaoModel", back_populates="produtos")

class MovimentacaoModel(Base):
    __tablename__ = "movimentacao"
    id_movimentacao = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(10), nullable=False)
    quantidade = Column(Integer, nullable=False)
    id_produto = Column(Integer, ForeignKey("produto.id_produto"), nullable=False)
    datetime_movimentacao = Column(DateTime, nullable=True)
    id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False)

    produto = relationship("ProdutoModel", back_populates="movimentacoes")
    user = relationship("UserModel", back_populates="movimentacoes")
    
    