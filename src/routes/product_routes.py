from fastapi import Depends, APIRouter

from models import User
from controllers import create_product, list_products, update_product
from schemas import CreateProductSchema, QueryProductSchema, UpdateProductSchema, ResponseProductSchema
from routes import get_current_user

product_router = APIRouter(prefix="/api/products")

@product_router.post(path="/create_product", response_model=ResponseProductSchema)
async def create_product_route(params: CreateProductSchema, current_user: User = Depends(get_current_user)):
    return create_product(current_user=current_user, params=params)


@product_router.post(path="/list_products", response_model=list[ResponseProductSchema])
async def list_products_route(params: QueryProductSchema, current_user: User = Depends(get_current_user)):
    return list_products(current_user=current_user, params=params)


@product_router.post(path="/update_product", response_model=ResponseProductSchema)
async def update_product_route(params: UpdateProductSchema, current_user: User = Depends(get_current_user)):
    return update_product(current_user=current_user, params=params)