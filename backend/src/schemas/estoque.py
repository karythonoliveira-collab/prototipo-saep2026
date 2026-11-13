from pydantic import BaseModel

class EstoqueCreate(BaseModel):
    nome: str
    preco_uni: float
    qtn: int

class EstoqueUpdate(BaseModel):
    nome: str | None = None
    preco_uni: float | None = None
    qtn: int | None = None

class MoveEstoque(BaseModel):
    qtn_move : int