from fastapi import APIRouter, HTTPException
from app.models.call_request import CallRequest
from app.services.vapi_service import VapiService

router = APIRouter()


@router.post("/create_call")
async def create_call(request: CallRequest):
    result = VapiService.create_call(request.model_dump(exclude_unset=True))
    if result["status"] == "success":
        print(result)
        return result
    else:
        raise HTTPException(status_code=400, detail=result["message"])
