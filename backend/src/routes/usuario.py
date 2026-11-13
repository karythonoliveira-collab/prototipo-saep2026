from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_sesion
from ..services import read_user, create_user, update_user, read_all_user, verificar_jwt_user, dellet_user
from ..schemas import UsuarioCreate, UsuarioUpdate

user_route = APIRouter(dependencies=Depends(verificar_jwt_user))

@user_route.get("/")
async def read_all_user_get(session: Session = Depends(get_sesion)):
    return read_all_user(session)

@user_route.get("/")
async def read_user_id(id: int = Depends(verificar_jwt_user), session: Session = Depends(get_sesion)):
    return read_user(session, id)

@user_route.post("/")
async def creat_user_post(base: UsuarioCreate,session: Session = Depends(get_sesion)):
    return create_user(session, base.nome, base.email, base.is_admin)

@user_route.put("/")
async def updade_user_post(base: UsuarioUpdate, id: int = Depends(verificar_jwt_user), session: Session = Depends(get_sesion)):
    return update_user(id, base.senha, base.nome, session)

@user_route.delete("/")
async def dellet_user_dellet(id: int = Depends(verificar_jwt_user),session: Session = Depends(get_sesion)):
    return dellet_user(id, session)



