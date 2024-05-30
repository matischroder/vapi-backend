import httpx
from fastapi import APIRouter, HTTPException, Depends

from app.auth.firebase_auth import verify_firebase_token
from app.models.data_models import AssistantPayload
from app.services.vapi_service import VapiService
from app.services.dynamo_db.assistants_service import DynamoDBAssistantsService

router = APIRouter()
dynamodb_service = DynamoDBAssistantsService()


@router.post(
    "/",
    dependencies=[Depends(verify_firebase_token)],
)
async def create_assistant(
    payload: AssistantPayload,
):
    try:
        vapi_response = await VapiService.create_assistant(payload.model_dump())
        dynamo_response = dynamodb_service.create_assistant(
            vapi_response.get("id"),
            payload.project_id,
            payload.first_message,
            payload.prompt,
            payload.voice_provider,
            payload.voice_id,
            payload.voice_speed,
        )

        return dynamo_response
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.get(
    "/project/{project_id}",
    dependencies=[Depends(verify_firebase_token)],
)
async def get_assistants_by_project(project_id: str):
    try:
        assistants = dynamodb_service.get_project_assistants(project_id)
        return assistants
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{assistant_id}",
    dependencies=[Depends(verify_firebase_token)],
)
async def get_assistant(assistant_id: str):
    try:
        assistant = dynamodb_service.get_assistant(assistant_id)
        if assistant:
            return assistant
        else:
            raise HTTPException(status_code=404, detail="Assistant not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch(
    "/{assistant_id}",
    dependencies=[Depends(verify_firebase_token)],
)
async def update_assistant(assistant_id: str, payload: AssistantPayload):
    try:
        dynamodb_service.update_assistant(assistant_id, payload.model_dump())
        await VapiService.update_assistant(assistant_id, payload.model_dump())
        return payload
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )


@router.delete(
    "/{assistant_id}",
    dependencies=[Depends(verify_firebase_token)],
)
async def delete_assistant(assistant_id: str):
    try:
        dynamodb_service.delete_assistant(assistant_id)
        await VapiService.delete_assistant(assistant_id)
        return assistant_id
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        )
