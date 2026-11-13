from typing import Literal
from pydantic import BaseModel

class EstoqueCreate(BaseModel):
    nome: str
    aplicacao: Literal["fundacao", "acabamento", "estrutura"]
    unidade_medida: Literal["uni", "kg", "litro", "m2"]
    preco_uni: float
    qtn: int
    qtn_minma: int
    obs: str | None = None

class EstoqueUpdate(BaseModel):
    nome: str | None = None
    aplicacao: Literal["fundacao", "acabamento", "estrutura"] | None = None
    unidade_medida: Literal["uni", "kg", "litro", "m2"] | None = None
    preco_uni: float | None = None
    qtn: int | None = None
    qtn_minma: int | None = None
    obs: str | None = None

