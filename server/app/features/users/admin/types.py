from strawberry import type
from typing import Optional
from datetime import date
from strawberry.experimental.pydantic import input as pydantic_input

from app.features.users.admin.models import CreatePg

@type
class Pg:
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    create_at: Optional[date] = None


@pydantic_input(model=CreatePg, all_fields=True)
class PgInput:
    pass