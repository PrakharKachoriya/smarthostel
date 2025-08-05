import strawberry
from strawberry.types import Info
from typing import AsyncGenerator
from app.logger import AppLogger
from app.core.pubsub import get_pub_sub
from app.graphql.analytics.types import (
    MealPending_PieChart,
    FloorWiseCount_DoubleBarChart,
    XAxis,
    YAxis
)

logger = AppLogger().get_logger()

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def pending_piechart(
        self,
        meal_type: str,
        info: Info
    ) -> AsyncGenerator[MealPending_PieChart, None]:
        """Subscribe to pie chart."""
        
        pubsub = get_pub_sub()
        pg_id = info.context["request"].headers.get("pg_id")
        async for message in pubsub.subscribe(f"{pg_id}__mealpending_piechart__{meal_type}"):
            yield MealPending_PieChart(**message)
    
    @strawberry.subscription
    async def floorwisecount_barchart(
        self,
        meal_type: str,
        floor: int,
        info: Info
    ) -> AsyncGenerator[FloorWiseCount_DoubleBarChart, None]:
        """Subscribe to bar chart."""
        
        pubsub = get_pub_sub()
        pg_id = info.context["request"].headers.get("pg_id")
        async for message in pubsub.subscribe(f"{pg_id}__roomwise_count_{floor}__{meal_type}"):
            message = message or {"x": {}, "y": {}}
            yield FloorWiseCount_DoubleBarChart(
                x=XAxis(**message.get("x", {})),
                y=YAxis(**message.get("y", {}))
            )
    