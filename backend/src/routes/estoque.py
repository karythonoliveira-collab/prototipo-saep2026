from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_sesion
from ..services import read_estoque, read_estoque_nome, saida_estoques, dellet_estoque, create_estoque, update_estoque, entrada_estoques, read_all_estoque, verificar_jwt_user
from ..schemas import EstoqueCreate, EstoqueUpdate, MoveEstoque

estoque_route = APIRouter(dependencies=Depends(verificar_jwt_user))

@estoque_route.get("/")
async def read_all_estoque_get(session: Session = Depends(get_sesion)):
    return read_all_estoque(session)

@estoque_route.get("/{id}")
async def read_estoque_id(id: int, session: Session = Depends(get_sesion)):
    return read_estoque(session, id)

@estoque_route.get("/{nome}")
async def read_estoque_id(nome: str, session: Session = Depends(get_sesion)):
    return read_estoque_nome(session, nome)

@estoque_route.delete("/{id}")
async def dellet_estoque_id(id: int, session: Session = Depends(get_sesion)):
    return dellet_estoque(id, session)

@estoque_route.post("/")
async def create_estoque_post(base: EstoqueCreate,session: Session = Depends(get_sesion)):
    return create_estoque(base.nome, base.preco_uni, base.qtn, session)

@estoque_route.put("/{id}")
async def estoque_updade_put(base: EstoqueUpdate,session: Session = Depends(get_sesion)):
    return update_estoque(base.nome, base.preco_uni, base.qtn, session)

@estoque_route.post("/{id}")
async def saida_estoque(id: int, base: MoveEstoque,session: Session = Depends(get_sesion), id_user :int = Depends(verificar_jwt_user)):
    return saida_estoques(id_user, id, base.qtn_move, session )

@estoque_route.psot("/{id}")
async def entrada_estoque(id: int, base: MoveEstoque,session: Session = Depends(get_sesion), id_user :int = Depends(verificar_jwt_user)):
    return entrada_estoques(id_user, id, base.qtn_move, session )






