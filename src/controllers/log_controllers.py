from sqlalchemy import select

from database import Session
from models import User, Product, Log
from schemas import QueryLogSchema, ResponseLogSchema
from errors import (
    UserNotFoundError, 
    InvalidProductQuantityError, 
    InvalidQueryError,
    LogNotFoundError,
    InvalidLogDateTimeError,
    )


def create_log(current_user: User, current_product: Product, initial_quantity: int, new_quantity: int) -> None:
    if new_quantity >= initial_quantity:
        log_type = "entry"
        quantity = new_quantity - initial_quantity
    else:
        log_type = "exit"
        quantity = initial_quantity - new_quantity

    new_log = Log(
        type=log_type,
        quantity=quantity,
        user_id=current_user.id,
        product_id=current_product.id
    )

    with Session() as session:
        session.add(new_log)
        session.commit()


def list_logs(current_user: User, params: QueryLogSchema) -> list[Log]:
    if current_user == None:
        raise UserNotFoundError
    
    if (params.minimum_quantity != None) and (params.minimum_quantity < 0):
        raise InvalidProductQuantityError
    
    if (params.maximum_quantity != None) and (params.maximum_quantity < 0):
        raise InvalidProductQuantityError
    
    if (params.minimum_quantity != None) and (params.maximum_quantity != None):
        if params.minimum_quantity > params.maximum_quantity:
            raise InvalidQueryError
    
    if (params.created_before != None) and (params.created_after != None):
        if params.created_after > params.created_before:
            raise InvalidLogDateTimeError
    
    stmt = select(Log)
    
    if params.id != None:
        stmt = stmt.where(Log.id == id)
    
    if params.type != None:
        stmt = stmt.where(Log.type == params.type)
    
    if params.minimum_quantity != None:
        stmt = stmt.where(Log.quantity >= params.minimum_quantity)
    
    if params.maximum_quantity != None:
        stmt = stmt.where(Log.quantity <= params.maximum_quantity)
    
    if params.created_before != None:
        stmt = stmt.where(Log.datetime >= params.created_before)
    
    if params.created_after != None:
        stmt = stmt.where(Log.datetime <= params.created_after)
    
    with Session() as session:
        logs = session.scalars(stmt).all()
    
    if logs == []:
        raise LogNotFoundError
    else:
        return logs

