from pydantic import BaseModel
class ProdutoCreate (BaseModel):
    nome: str
    quantidade: int
    preco: float


