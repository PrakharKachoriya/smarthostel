import strawberry
from typing import Optional
from datetime import datetime


@strawberry.type
class Tenant:
    id: str
    name: str
    email: str
    room_number: int
    kyc: bool = False


@strawberry.type
class MealActivity:
    tenant_id: str
    room_number: int
    meal_type: str
    timestamp: datetime | None = None # Can be also managed in SQL as CURRENT_TIMESTAMP
    rating: int | None = None # Rating is to be added later, defaulting to None


@strawberry.input
class TenantInput:
    id: str
    name: str
    email: str
    room_number: int
    kyc: Optional[bool] = False


@strawberry.input
class MealActivityInput:
    tenant_id: str
    room_number: int
    meal_type: str
    timestamp: datetime | None = None
    rating: int | None = None