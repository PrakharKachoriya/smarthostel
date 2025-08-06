from pydantic import BaseModel
from typing import Optional
from datetime import date


class CreateTenant(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    floor: int
    room_number: str
    join_date: Optional[date] = None