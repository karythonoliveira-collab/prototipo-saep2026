from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr

class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    role: Literal["operator", "admin"]



class LoginUserSchema(BaseModel):
    email: EmailStr
    password: SecretStr



class ResponseUserSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: EmailStr
    password: SecretStr
    role: Literal["operator", "admin"]


