from datetime import date
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class ProdutoEntrada(BaseModel):
    nome : str = Field(min_length =1, max_length=100)
    quantidade_estoque: int = Field(default=0, ge=0)
    valor_unitario: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    estoque_minimo: int = Field(default=10, ge=0)

class ProdutoEdicao(BaseModel):
    nome : str = Field(min_length=1, max_length=100)
    valor_unitario: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    estoque_minimo: int = Field(ge=0)

class MovimentacaoEntrada(BaseModel):
    id_produto: int = Field(gt=0)
    tipo : Literal['ENTRADA', 'SAIDA']
    quantidade : int = Field(gt=0)

class ProdutoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome : str 
    quantidade_estoque : int 
    valor_unitario : Decimal
    estoque_minimo: int
    data_cadastro: date
    valor_total: Decimal
