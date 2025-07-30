from strawberry import Schema
from strawberry.fastapi import GraphQLRouter
from fastapi import Request

from app.graphql.db.query import Query
from app.graphql.db.mutation import Mutation
from app.graphql.analytics.subscriptions import Subscription

schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)

async def get_context(request: Request):
    return {"request": request}

graphql_router = GraphQLRouter(schema, context_getter=get_context)