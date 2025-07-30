from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreateTenant(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    room_number: int
    payment_pending: bool = True
    join_date: Optional[date] = None