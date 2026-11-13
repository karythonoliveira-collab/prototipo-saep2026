from pydantic import BaseModel, ConfigDict
from typing import Optional

class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserLoginSchema(Schema):
    email: str
    senha: str


class UserCreateSchema(Schema):
    nome: str
    email: str
    senha: str

class UserResponseSchema(Schema):
    id: int
    nome: str
    email: str

class ItemCreateSchema(Schema):
    nome: str
    validade: Optional[str] = None
    cor: Optional[str] = None
    quantidade: float = 0.0
    unidade: str = "un"

class ItemUpdateSchema(Schema):
    nome: str
    validade: Optional[str] = None
    cor: Optional[str] = None
    unidade: str = "un"

class MovimentacaoSchema(Schema):
    usuario_id: int
    item_id: int
    tipo: str
    quantidade: float
    data: str
