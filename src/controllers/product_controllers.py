from typing import Optional

from sqlalchemy import select

from database import Session
from models import User, Product
from schemas import CreateProductSchema, QueryProductSchema, UpdateProductSchema
from errors import (
    UserNotFoundError, 
    UserHasNoPermissionError, 
    ProductNotFoundError, 
    InvalidProductQuantityError, 
    InvalidProductValueError,
    InvalidQueryError,
    )
from controllers import create_log

def get_product_by_id(id: int) -> Optional[Product]:
    stmt = select(Product).where(Product.id == id)

    with Session() as session:
        target_product = session.scalar(stmt)

    return target_product


def create_product(current_user: User, params: CreateProductSchema) -> Product:
    if current_user == None:
        raise UserNotFoundError

    if params.quantity < 0:
        raise InvalidProductQuantityError

    if params.value < 0:
        raise InvalidProductValueError

    new_product = Product(
        description=params.description,
        quantity=params.quantity,
        value=params.value,
    )

    with Session() as session:
        session.add(new_product)
        session.commit()

    return new_product


def list_products(current_user: User, params: QueryProductSchema) -> list[Product]:
    if current_user == None:
        raise UserNotFoundError

    if (params.minimum_quantity != None) and (params.minimum_quantity < 0):
        raise InvalidProductQuantityError

    if (params.maximum_quantity != None) and (params.maximum_quantity < 0):
        raise InvalidProductQuantityError

    if (params.minimum_value != None) and (params.minimum_value < 0):
        raise InvalidProductValueError

    if (params.maximum_value != None) and (params.maximum_value < 0):
        raise InvalidProductValueError

    if (params.minimum_quantity != None) and (params.maximum_quantity != None):
        if params.minimum_quantity > params.maximum_quantity:
            raise InvalidQueryError

    if (params.minimum_value != None) and (params.maximum_value != None):
        if params.minimum_value > params.maximum_value:
            raise InvalidQueryError

    stmt = select(Product)

    if params.id != None:
        stmt = stmt.where(Product.id == id)

    if params.description != None:
        stmt = stmt.where(params.description in Product.description)

    if params.minimum_quantity != None:
        stmt = stmt.where(Product.quantity >= params.minimum_quantity)

    if params.maximum_quantity != None:
        stmt = stmt.where(Product.quantity <= params.maximum_quantity)

    if params.minimum_value != None:
        stmt = stmt.where(Product.value >= params.minimum_value)

    if params.maximum_value != None:
        stmt = stmt.where(Product.value <= params.maximum_value)

    if params.created_before != None:
        stmt = stmt.where(Product.created_at >= params.created_before)

    if params.created_after != None:
        stmt = stmt.where(Product.created_at <= params.created_after)

    with Session() as session:
        products = session.scalars(stmt).all()

    if products == []:
        raise ProductNotFoundError
    else:
        return products


def update_product(current_user: User, params: UpdateProductSchema) -> Product:
    if current_user == None:
        raise UserNotFoundError

    if params.quantity < 0:
        raise InvalidProductQuantityError

    if params.value < 0:
        raise InvalidProductValueError

    target_product = get_product_by_id(id=params.id)

    if target_product == None:
        raise ProductNotFoundError

    with Session() as session:
        if params.description != None:
            target_product.description = params.description

        if params.quantity != None:
            create_log(
                current_user=current_user, 
                current_product=target_product,
                initial_quantity=target_product.quantity,
                new_quantity=params.quantity 
            )
            target_product.quantity = params.quantity

        if params.value != None:
            target_product.value = params.value

        session.commit()

    return target_product