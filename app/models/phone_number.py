from pydantic import BaseModel


class PhoneNumber(BaseModel):
    number: str
    id: str
