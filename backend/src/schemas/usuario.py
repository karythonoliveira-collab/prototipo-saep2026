from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    senha: str
    email: str
    is_admin: bool

class UsuarioUpdate(BaseModel):
    senha: str | None = None
    nome: str | None = None


