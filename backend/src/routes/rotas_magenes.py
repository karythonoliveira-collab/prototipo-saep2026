from fastapi.responses import RedirectResponse
from fastapi import APIRouter
from .usuario import user_route

manger_route = APIRouter()

#caso entre na url root acaba sendo jogado para /docs d aapi
@manger_route.get("/",include_in_schema=False)
async def home_to_doc():
    return RedirectResponse(url='/docs')

manger_route.include_router(
    user_route,
    prefix="/user"
)



