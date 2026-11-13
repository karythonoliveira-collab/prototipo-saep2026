from datetime import Date, date, datetime
from pydantic import ConfigDict, BaseModel, EmailStr, Field
from decimal import Decimal

class UsuarioCreate(BaseModel):
    id_user = int
    nome = str
    email = EmailStr
    senha = str
    perfil = str

class UsuarioUpdate(BaseModel):
    nome = str | None = None
    email = EmailStr | None = None
    senha = str | None = None 
    perfil = str | None = None

class UsuarioResponse(BaseModel):
    id_user = int
    nome = str
    email = EmailStr
    perfil = str

    model_config = ConfigDict(from_attributes=True)

class ProdutoCreate(BaseModel):
    nome = str
    quantidade_estoque = int
    valor_uni = Decimal

class ProdutoUpdate(BaseModel):
    nome = str | None = None
    quantidade_estoque = int | None = None
    valor_uni = Decimal | None = None

class ProdutoResponse(BaseModel):
    nome = str
    quantidade_estoque = int
    valor_uni = Decimal
    data_cadastro = date

    model_config = ConfigDict(from_attributes=True)

class MovimentacaoCreate(BaseModel):
    tipo = str
    quantidade = int
    id_produto = int
    id_user = int

class MovimentacaoResponse(BaseModel):
    id_movimentacao = int
    datetime_movimentacao = datetime
    tipo = str
    quantidade = int
    id_produto = int
    id_user = int

    model_config = ConfigDict(from_attributes=True)