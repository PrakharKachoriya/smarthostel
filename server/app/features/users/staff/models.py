from pydantic import BaseModel


class CreateStaff(BaseModel):
    name: str
    password: str
    phone_number: str
    role: str