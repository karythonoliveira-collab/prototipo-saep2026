from typing import Literal, Optional
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class CreateProductSchema(BaseModel):
    description: str
    quantity: int
    value: Decimal



class QueryProductSchema(BaseModel):
    id = Optional[int] = None
    description: Optional[str] = None
    minimum_quantity: Optional[int] = None
    maximum_quantity: Optional[int] = None
    minimum_value: Optional[Decimal] = None
    maximum_value: Optional[Decimal] = None
    created_before: Optional[datetime] = None
    created_after: Optional[datetime] = None



class ResponseProductSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    description: str
    quantity: int
    value: Decimal
    created_at = datetime


