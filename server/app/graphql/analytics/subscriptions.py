import strawberry
from typing import AsyncGenerator
from app.core.pubsub import get_pub_sub
from app.graphql.analytics.types import (
    MealPending_PieChart,
    MealTime_LineChart,
    FoodRating_LineChart,
    FloorWiseCount_DoubleBarChart,
)

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def pending_piechart(self, meal_type: str) -> AsyncGenerator[MealPending_PieChart, None]:
        """Subscribe to pie chart."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"mealpending_piechart_{meal_type}"):
            yield MealPending_PieChart(**message)
    
    @strawberry.subscription
    async def floorwisecount_barchart(self, meal_type: str, floor: int) -> AsyncGenerator[FloorWiseCount_DoubleBarChart, None]:
        """Subscribe to bar chart."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"floorwisecount_barchart_{meal_type}_floor_{floor}"):
            yield FloorWiseCount_DoubleBarChart(**message)
    
    @strawberry.subscription
    async def mealtime_linechart(self, meal_type: str) -> AsyncGenerator[MealTime_LineChart, None]:
        """Subscribe to line chart."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"mealtime_linechart_{meal_type}"):
            yield MealTime_LineChart(**message)
    
    @strawberry.subscription
    async def foodrating_linechart(self, meal_type: str) -> AsyncGenerator[FoodRating_LineChart, None]:
        """Subscribe to line chart."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"foodrating_linechart_{meal_type}"):
            yield FoodRating_LineChart(**message)