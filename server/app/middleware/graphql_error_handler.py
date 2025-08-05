# middlewares.py
from strawberry.types import Info
from graphql import GraphQLError
from app.core.exceptions.base import BaseAppException

async def graphql_exception_handler(resolve, root, info: Info, *args, **kwargs):
    try:
        return await resolve(root, info, *args, **kwargs)
    except BaseAppException as exc:
        raise GraphQLError(
            message=exc.message,
            extensions={"status": exc.status, "code": exc.code}
        )
    except Exception as exc:
        # Optional: handle unexpected exceptions
        raise GraphQLError(
            message="Internal server error",
            extensions={"status": "INTERNAL_SERVER_ERROR", "code": 500}
        )
