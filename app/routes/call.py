from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.vapi_service import VapiService

router = APIRouter()


class CallRequest(BaseModel):
    firstMessage: Optional[str] = None
    context: Optional[str] = None
    voice: Optional[str] = None
    phone_number_id: Optional[str] = None
    customer_number: Optional[str] = None
    agent_id: Optional[str] = None


@router.post("/create_call")
async def create_call(request: CallRequest):
    result = VapiService.create_call(request.model_dump(exclude_unset=True))
    if result["status"] == "success":
        print(result)
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])
