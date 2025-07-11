from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import router as db_router
from app.analytics import router as analytics_router
from app.logger import AppLogger

AppLogger("app")
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(db_router.router, prefix="/db")
app.include_router(analytics_router.router, prefix="/analytics")