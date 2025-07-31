import strawberry
from typing import AsyncGenerator, Any
from app.logger import AppLogger
from app.core.pubsub import get_pub_sub
from app.graphql.analytics.types import (
    MealPending_PieChart,
    MealTime_LineChart,
    FoodRating_LineChart,
    FloorWiseCount_DoubleBarChart,
    Message
)
from app.graphql.db.types import Tenant

logger = AppLogger().get_logger()

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def pending_piechart(
        self,
        pg_key: str,
        meal_type: str
    ) -> AsyncGenerator[list[MealPending_PieChart], None]:
        """Subscribe to pie chart."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"{pg_key}_mealpending_piechart_{meal_type}"):
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
    
    @strawberry.subscription
    async def task_1_listener(self, meal_type: str) -> AsyncGenerator[Message, None]:
        """Subscribe to task 1 updates."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"task_1_{meal_type}"):
            logger.debug(f"Received message for task 1: {message}")
            yield Message(message=[Tenant(**row) for row in message])
    
    @strawberry.subscription
    async def task_2_listener(self, meal_type: str) -> AsyncGenerator[Message, None]:
        """Subscribe to task 2 updates."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"task_2_{meal_type}"):
            logger.debug(f"Received message for task 2: {message}")
            yield Message(message=[Tenant(**row) for row in message])
    
    @strawberry.subscription
    async def task_3_listener(self, meal_type: str) -> AsyncGenerator[Message, None]:
        """Subscribe to task 3 updates."""
        
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"task_3_{meal_type}"):
            logger.debug(f"Received message for task 3: {message}")
            yield Message(message=[Tenant(**row) for row in message])