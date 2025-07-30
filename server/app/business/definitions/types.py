from pydantic import BaseModel
from typing import Optional
from datetime import date

class CreateTenant(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    room_number: int
    join_date: Optional[date] = None


class CreatePg(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    address: str
    city: str
    state: str
    postal_code: str


class CreateStaff(BaseModel):
    name: str
    password: str
    phone_number: str
    role: str