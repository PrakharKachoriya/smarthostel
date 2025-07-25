import strawberry
from typing import Optional


@strawberry.type
class Tenant:
    id: str
    name: str
    email: str
    room_number: int
    kyc: bool = False


@strawberry.type
class MealActivity:
    tenant_id: int
    room_number: int
    meal_type: str
    timestamp: float | None = None
    rating: int | None = None


@strawberry.input
class TenantInput:
    id: int
    name: str
    email: str
    room_number: int


@strawberry.input
class MealActivityInput:
    tenant_id: int
    room_number: int
    meal_type: str
    timestamp: Optional[float | None] = None
    rating: Optional[int] = 3