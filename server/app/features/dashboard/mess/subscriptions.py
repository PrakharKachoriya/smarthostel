# import strawberry
# from strawberry.types import Info
# from typing import AsyncGenerator
# from app.logger import AppLogger
# from app.core.pubsub import get_pub_sub
# from types import (
#     MealPending_PieChart,
#     FloorWiseCount_DoubleBarChart,
#     XAxis,
#     YAxis
# )
#
#
# logger = AppLogger().get_logger()
#
# @strawberry.type
# class TenantSubscription:
#     @strawberry.subscription
#     async def mealpending_piechart(
#             self,
#             meal_type: str,
#             info: Info
#     ) -> AsyncGenerator[MealPending_PieChart]:
#         """Subscribe to pie chart."""
#
#         pg_id = info.context["pg_id"]
#         pubsub = get_pub_sub()
#         async for message in pubsub.subscribe(f"{pg_id}__mealpending_piechart__{meal_type}"):
#             message = message or {"label": [], "values": []}
#             yield MealPending_PieChart(**message)
#
#     @strawberry.subscription
#     async def floorwisecount_barchart(
#             self,
#             meal_type: str,
#             floor: int,
#             info: Info
#     ) -> AsyncGenerator[FloorWiseCount_DoubleBarChart]:
#         """Subscribe to bar chart."""
#
#         pg_id = info.context["pg_id"]
#         pubsub = get_pub_sub()
#         async for message in pubsub.subscribe(f"{pg_id}__roomwise_count_{floor}__{meal_type}"):
#             message = message or {"x": {}, "y": {}}
#             yield FloorWiseCount_DoubleBarChart(
#                 x=XAxis(**message["x"]),
#                 y=YAxis(**message["y"])
#             )