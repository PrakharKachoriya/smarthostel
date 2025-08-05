import strawberry
from typing import Optional
from datetime import date
from strawberry.experimental.pydantic import input as pydantic_input

from app.features.users.tenant.models import CreateTenant

@strawberry.type
class Tenant:
    id: Optional[str] = None
    pg_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    room_number: Optional[str] = None
    floor: Optional[int] = None
    join_date: Optional[date] = None
    created_at: Optional[date] = None


@strawberry.input
class GetTenant:
    id: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


@pydantic_input(model=CreateTenant, all_fields=True)
class TenantInput:
    pass