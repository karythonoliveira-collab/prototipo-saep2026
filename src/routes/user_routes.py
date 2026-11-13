from fastapi import APIRouter

from controllers import create_user, login
from schemas import CreateUserSchema, LoginUserSchema, ResponseUserSchema

user_router = APIRouter(prefix="/api/users")

@user_router.post(path="/create_user", response_model=ResponseUserSchema)
async def create_user_route(params: CreateUserSchema):
    return create_user(params=params)


@user_router.post(path="/login", response_model=ResponseUserSchema)
async def login_route(params: LoginUserSchema):
    return login(params=params)


