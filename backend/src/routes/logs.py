from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_sesion
from ..services import read_all_logs, verificar_jwt_user

logs_route = APIRouter(dependencies=Depends(verificar_jwt_user))

@logs_route.get("/")
async def read_all_logs_get(session: Session = Depends(get_sesion)):
    return read_all_logs(session)


