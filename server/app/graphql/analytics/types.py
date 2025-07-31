import strawberry

from app.graphql.db.types import Tenant

@strawberry.type
class MealPending_PieChart:
    labels: list[str]
    values: list[int]

@strawberry.type
class MealTime_LineChart:
    time_values: list[float]
    values: list[int]

@strawberry.type
class FoodRating_LineChart:
    ratings: list[int]
    counts: list[int]

@strawberry.type
class FloorWiseCount_DoubleBarChart:
    floors: list[int]
    status_wise_counts: list[tuple[int, int]]


@strawberry.type
class Message:
    message: list[Tenant]