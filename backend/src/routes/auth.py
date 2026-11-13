from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import get_sesion
from ..schemas import UsuarioCreate
from ..services import create_user, login_user 

auth_route = APIRouter()


@auth_route.post("/creat_acout")
async def Criar_Conta(base: UsuarioCreate, session: Session = Depends(get_sesion)):
    return create_user(base.nome,base.senha,base.email, base.is_admin, session)

@auth_route.post("/login_acout")
async def Logar_Conta(base: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_sesion)):
    '''\nRealiza o login do cliente e retorna um token JWT. \n \n \
    O username = email \n \n \
    O password = senha \n \n \
    '''

    return login_user(base.username, base.password, session)





