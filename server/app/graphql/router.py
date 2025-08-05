from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from app.graphql.context import get_context
# v1
from app.graphql.db.query import Query
from app.graphql.db.mutation import Mutation
from app.graphql.analytics.subscriptions import Subscription

#v2
from app.graphql.queries import Query as Query_v2
from app.graphql.mutations import Mutation as Mutation_v2
from app.middleware.graphql_error_handler import graphql_exception_handler


schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)
graphql_router = GraphQLRouter(schema, context_getter=get_context)

schema_v2 = Schema(query=Query_v2, mutation=Mutation_v2)
graphql_router_v2 = GraphQLRouter(
    schema_v2,
    context_getter=get_context,
    # middleware={graphql_exception_handler}
)