from pydantic import BaseModel
from typing import List, Optional


class AgentRequest(BaseModel):
    agent_id: str
    first_message: str
    model_provider: str = "openai"
    model_name: str = "gpt-3.5-turbo"
    voice: str = "jennifer-playht"


class CallRequest(BaseModel):
    phone_number_id: str
    customer_number: str
    agent_id: str


class PhoneNumber(BaseModel):
    number: str
    id: str


class Project(BaseModel):
    project_id: str
    vapi_phone_numbers: Optional[List[PhoneNumber]] = []
