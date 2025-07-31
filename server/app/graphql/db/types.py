import strawberry
from strawberry.experimental.pydantic import input as pydantic_input
from typing import Optional
from datetime import date, datetime

from app.business.definitions.types import (
    CreatePg,
    CreateTenant,
    CreateStaff,
    CreateQRScanLog
)

@strawberry.type
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

@strawberry.type
class Tenant:
    id: Optional[str] = None
    pg_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    room_number: Optional[int] = None
    join_date: Optional[date] = None
    created_at: Optional[date] = None

@strawberry.type
class Staff:
    id: Optional[str] = None
    pg_id: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[date] = None
    
@strawberry.type
class QRScanLog:
    id: Optional[str]
    pg_id: Optional[str]
    tenant_id: Optional[str] = None
    meal_type: Optional[str] = None
    curr_timestamp: Optional[datetime] = None # Can be also managed in SQL as CURRENT_TIMESTAMP
    curr_date: Optional[date] = None

@pydantic_input(model=CreatePg, all_fields=True)
class PgInput:
    pass

@pydantic_input(model=CreateTenant, all_fields=True)
class TenantInput:
    pass

@pydantic_input(model=CreateStaff, all_fields=True)
class StaffInput:
    pass

@pydantic_input(model=CreateQRScanLog, all_fields=True)
class QRScanLogInput:
    pass