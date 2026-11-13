from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import jwt, JWTError
from datetime import datetime

from ..config import SECRETES_KEY, ALG, TIMER  
from .erros import ErroInesperado, JwtInvalido, JustAdmin

oauth_schema = OAuth2PasswordBearer('/auth/login_acout')

def criar_token(id_user: int,  is_admin : bool= False) -> str:
    try:
        dt_expi = datetime.now + TIMER

        dic_info = None

        #O dic_info está configurado com base no padrão JWT: https://www.jwt.io/
        dic_info = {'sub': str(id_user),'exp': dt_expi, "is_admin" : is_admin,}
        
        jwt_codificado = jwt.encode(dic_info, SECRETES_KEY, ALG)#type: ignore
        return jwt_codificado
    
    except Exception as e:
        raise ErroInesperado(e)

def verificar_jwt(token: str) -> tuple:
    try:
        dict_info = jwt.decode(token, str(SECRETES_KEY), str(ALG))
        id = int(dict_info['sub'])
        is_admin = bool(dict_info["is_admin"])

        return id, is_admin
    
    except JWTError:
        raise JwtInvalido()
    
    except Exception as e:
        raise ErroInesperado(e)

def verificar_jwt_user(token = Depends(oauth_schema)) -> int:
    try:
        id, _, = verificar_jwt(token)
    
        return int(id)

    except (JwtInvalido): raise
    
    except Exception as e: 
        raise ErroInesperado(e)

def verificar_jwt_admin(token = Depends(oauth_schema)) -> int:
    try:
        id, is_admin, = verificar_jwt(token)
        

        if is_admin == True: return int(id)

        else: raise JustAdmin()

    
    except (JwtInvalido, JustAdmin): raise

    except Exception as e: 
        raise ErroInesperado(e)

