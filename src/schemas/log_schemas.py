from typing import Literal, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class QueryLogSchema(BaseModel):
    id: Optional[int] = None
    type: Optional[Literal["entry", "exit"]] = None
    minimum_quantity: Optional[int] = None
    maximum_quantity: Optional[int] = None
    created_before: Optional[datetime] = None
    created_after: Optional[datetime] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None



class ResponseLogSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    type: Literal["entry", "exit"]
    quantity: int
    datetime: datetime

    user_id: int
    product_id: int



