import strawberry
from typing import List, Optional
from app.graphql.db.types import Tenant

@strawberry.type
class MealPending_PieChart:
    labels: list[str]
    values: list[int]


@strawberry.type
class XAxis:
    room_numbers: List[int]

@strawberry.type
class YAxis:
    pending: Optional[List[int]] = None
    served: Optional[List[int]] = None

@strawberry.type
class FloorWiseCount_DoubleBarChart:
    x: XAxis
    y: YAxis