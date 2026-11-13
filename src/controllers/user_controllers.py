from typing import Optional

from sqlalchemy import select

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from database import Session
from models import User
from schemas import CreateUserSchema, LoginUserSchema
from errors import UserAlreadyExistsError, UserNotFoundError, InvalidUserDataError

argon2 = PasswordHasher()

def get_user_by_email(email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)

    with Session() as session:
        target_user = session.scalar(stmt)

    return target_user


def verify_password(hashed_password: str, target_password: str) -> bool:
    try:
        argon2.verify(hash=hashed_password, password=target_password)
        return True
    
    except VerifyMismatchError:
        return False
    

def create_user(params: CreateUserSchema) -> User:
    if get_user_by_email(email=params.email.lower()) != None:
        raise UserAlreadyExistsError

    password = params.password.get_secret_value()

    if len(password) < 6:
        raise InvalidUserDataError

    new_user = User(
        name=params.name,
        email=params.email.lower(),
        password=argon2.hash(password=password),
        role=params.role
    )

    with Session() as session:
        session.add(new_user)
        session.commit()

    return new_user


def login(params: LoginUserSchema) -> User:
    target_user = get_user_by_email(email=params.email.lower())
    
    if target_user == None:
        raise UserNotFoundError

    password = params.password.get_secret_value()

    if verify_password(hashed_password=target_user.password, target_password=password) == False:
        raise InvalidUserDataError

    return target_user