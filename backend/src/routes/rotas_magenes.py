from fastapi.responses import RedirectResponse
from fastapi import APIRouter
from .usuario import user_route
from .auth import auth_route
from .estoque import estoque_route
from .logs import logs_route

manger_route = APIRouter()

#caso entre na url root acaba sendo jogado para /docs d aapi
@manger_route.get("/",include_in_schema=False)
async def home_to_doc():
    return RedirectResponse(url='/docs')

manger_route.include_router(
    auth_route,
    prefix="/auth",
    tags=["atuh", "user"]
)

manger_route.include_router(
    user_route,
    prefix="/user",
    tags=["user"]
)

manger_route.include_router(
    estoque_route,
    prefix="/estoque",
    tags=["estoque"]
)

manger_route.include_router(
    logs_route,
    prefix="/logs_route",
    tags=["movementação"]
)



