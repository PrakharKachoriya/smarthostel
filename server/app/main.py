from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.logger import AppLogger
from app.graphql.analytics.aggregator import lifespan
from app.graphql.router import graphql_router

AppLogger("app")
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_router, prefix="/graphql")