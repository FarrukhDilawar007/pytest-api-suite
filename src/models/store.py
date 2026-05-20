from typing import Optional
from pydantic import BaseModel


class Order(BaseModel):
    id: Optional[int] = None
    petId: Optional[int] = None
    quantity: Optional[int] = None
    shipDate: Optional[str] = None
    status: Optional[str] = None
    complete: Optional[bool] = None
