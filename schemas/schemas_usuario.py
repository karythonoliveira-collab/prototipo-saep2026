from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    admin: bool

class UsuarioEdit(BaseModel):
    id_usuario: int