from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from app.graphql.db.query import Query
from app.graphql.db.mutation import Mutation
from app.graphql.analytics.subscriptions import Subscription

schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)

graphql_router = GraphQLRouter(schema)