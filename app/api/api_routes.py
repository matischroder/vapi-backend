from fastapi import APIRouter, Depends
from app.services.external_api_service import fetch_external_data
from typing import Any

router = APIRouter()


@router.get("/data", response_model=Any)
async def get_data(param: str):
    data = await fetch_external_data(param)
    return data
