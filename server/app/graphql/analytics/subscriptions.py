import strawberry
from app.core.pubsub import get_pub_sub

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def pending_piechart(self, meal_type: str) -> dict:
        """Subscribe to pie chart."""
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"mealpending_piechart_{meal_type}"):
            yield message
    
    @strawberry.subscription
    async def floorwisecount_barchart(self, meal_type: str, floor: int) -> dict:
        """Subscribe to bar chart."""
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"floorwisecount_barchart_{meal_type}_floor_{floor}"):
            yield message
    
    @strawberry.subscription
    async def mealtime_linechart(self, meal_type: str) -> dict:
        """Subscribe to line chart."""
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"mealtime_linechart_{meal_type}"):
            yield message
    
    @strawberry.subscription
    async def foodrating_linechart(self, meal_type: str) -> dict:
        """Subscribe to line chart."""
        pubsub = get_pub_sub()
        async for message in pubsub.subscribe(f"foodrating_linechart_{meal_type}"):
            yield message