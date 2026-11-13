from pydantic import BaseModel

class MovimentaçãoRegistro(BaseModel):
    tipo: str
    quantidade: int
    valot: float
    id_produto: int
    id_usuario: int
    data:str
