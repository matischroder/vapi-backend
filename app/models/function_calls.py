from pydantic import BaseModel


class FunctionCallRequest(BaseModel):
    message: dict


class UserData(BaseModel):
    project_id: str
    campaign_id: str
    user_phone_number: str
    total_debt_amount: float
