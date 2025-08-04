import strawberry
from typing import Optional
from datetime import date, datetime
from strawberry.experimental.pydantic import input as pydantic_input

from app.features.dashboard.mess.models import CreateQRScanLog


@strawberry.type
class QRScanLog:
    id: Optional[str]
    pg_id: Optional[str]
    tenant_id: Optional[str] = None
    meal_type: Optional[str] = None
    curr_timestamp: Optional[datetime] = None # Can be also managed in SQL as CURRENT_TIMESTAMP
    curr_date: Optional[date] = None


@strawberry.input
class GetQRScanLog:
    tenant_id: Optional[str] = None
    meal_type: Optional[str] = None
    curr_date: Optional[date] = None


@pydantic_input(model=CreateQRScanLog, all_fields=True)
class QRScanLogInput:
    pass