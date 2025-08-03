from strawberry import type
from typing import Optional
from datetime import date
from strawberry.experimental.pydantic import input as pydantic_input

from app.features.users.staff.models import CreateStaff


@type
class Staff:
    id: Optional[str] = None
    pg_id: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[date] = None

@type
class GetStaff:
    id: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


@pydantic_input(model=CreateStaff, all_fields=True)
class StaffInput:
    pass