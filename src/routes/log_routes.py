from fastapi import Depends, APIRouter

from models import User
from controllers import list_logs
from schemas import QueryLogSchema, ResponseLogSchema
from routes import get_current_user

log_router = APIRouter(prefix="/api/logs")

@log_router.post("/list_logs", response_model=list[ResponseLogSchema])
async def list_logs_route(params: QueryLogSchema, current_user: User = Depends(get_current_user)):
    return list_logs(current_user=current_user, params=params)



