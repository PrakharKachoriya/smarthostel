from pydantic import BaseModel

class CreatePg(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    address: str
    city: str
    state: str
    postal_code: str