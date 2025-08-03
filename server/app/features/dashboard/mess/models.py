from pydantic import BaseModel


class CreateQRScanLog(BaseModel):
    tenant_id: str
    meal_type: str