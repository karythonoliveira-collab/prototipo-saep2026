from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    senha: str
    email: str

class UsuarioUpdate(BaseModel):
    senha: str | None = None
    nome: str | None = None


