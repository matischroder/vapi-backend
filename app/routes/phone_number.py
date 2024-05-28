import httpx
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request

from app.auth.firebase_auth import verify_firebase_token
from app.models.data_models import PhoneNumber
from app.services.vapi_service import VapiService
from app.services.dynamo_db.phone_number_service import DynamoDBPhoneService

router = APIRouter()
dynamo_service = DynamoDBPhoneService()


@router.get(
    "/{project_id}",
    dependencies=[Depends(verify_firebase_token)],
    response_model=List[PhoneNumber],
)
async def get_phone_numbers(project_id: str):
    return dynamo_service.get_project_phone_numbers(project_id)


@router.post("/buy", dependencies=[Depends(verify_firebase_token)])
async def buy_phone_number(request: Request, project_id: str, area_code: str):
    try:
        decoded_token = request.state.user_data
        if not decoded_token["email"].endswith("@bircle.ai"):
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Por favor solicite a un administrador para comprar un nuevo número"
                },
            )
        response = await VapiService.buy_phone_number(area_code)
        phone_number = PhoneNumber(number=response["number"], id=response["id"])
        phone_numbers = dynamo_service.get_project_phone_numbers(project_id)
        phone_numbers.append(phone_number)
        dynamo_service.update_project_phone_numbers(project_id, phone_numbers)
        return phone_number
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.post("/import_twilio", dependencies=[Depends(verify_firebase_token)])
async def import_twilio(
    project_id: str,
    project_name: str,
    phone_number: str,
    twilio_account_sid: str,
    twilio_auth_token: str,
):
    try:
        response = await VapiService.import_twilio(
            phone_number, twilio_account_sid, twilio_auth_token, project_name
        )
        phone_number = {"number": response["number"], "id": response["id"]}
        phone_numbers = dynamo_service.get_project_phone_numbers(project_id)
        phone_numbers.append(phone_number)
        dynamo_service.update_project_phone_numbers(project_id, phone_numbers)
        return phone_number
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.post("/import_vonage", dependencies=[Depends(verify_firebase_token)])
async def import_vonage(
    project_id: str, project_name: str, phone_number: str, credential_id: str
):
    try:
        response = await VapiService.import_vonage(
            phone_number, credential_id, project_name
        )
        phone_number = PhoneNumber(number=response["number"], id=response["id"])
        phone_numbers = dynamo_service.get_project_phone_numbers(project_id)
        phone_numbers.append(phone_number)
        dynamo_service.update_project_phone_numbers(project_id, phone_numbers)
        return phone_number
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.delete(
    "/{project_id}/{phone_id}", dependencies=[Depends(verify_firebase_token)]
)
async def delete_phone_number(project_id: str, phone_id: str):
    phone_numbers = dynamo_service.get_project_phone_numbers(project_id)
    phone_number_obj = next((pn for pn in phone_numbers if pn["id"] == phone_id), None)
    if not phone_number_obj:
        raise HTTPException(status_code=404, detail="Phone number not found in project")

    try:
        await VapiService.delete_phone_number(phone_number_obj["id"])
        phone_numbers = [pn for pn in phone_numbers if pn["id"] != phone_id]
        dynamo_service.update_project_phone_numbers(project_id, phone_numbers)
        return {"message": "Phone number deleted successfully"}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
