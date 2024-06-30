from pydantic import BaseModel
from typing import Optional


class CallRequest(BaseModel):
    firstMessage: Optional[str] = None
    context: Optional[str] = None
    voice: Optional[str] = None
    phone_number_id: Optional[str] = None
    customer_number: Optional[str] = None
    agent_id: Optional[str] = None
