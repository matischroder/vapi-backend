import json
from datetime import date, datetime
from fastapi import APIRouter, HTTPException

from app.storage import storage
from app.models.function_calls import FunctionCallRequest
from app.models.call import Call
from app.utils.get_user_info import get_user_info
from app.services.vapi_service import VapiService
from app.services.dynamo_db.payment_promises import DynamoDBPromiseService

router = APIRouter()
payment_promise_dynamo_service = DynamoDBPromiseService()


@router.post("")
async def function_call(request: FunctionCallRequest):
    try:
        data = request.message
        customer_number = data.get("customer", {}).get("number")
        if not customer_number:
            return "Hubo un error para encontrar sus datos, lo llamaremos nuevamente brevemente"

        print(f"Customer number: {customer_number}")
        print(f"Storage calls: {storage.calls}")

        if customer_number not in storage.calls:
            return "Hubo un error para encontrar sus datos, lo llamaremos nuevamente brevemente"

        current_call: Call = storage.calls[customer_number]
        print(f"Current call: {current_call}")

        response = current_call.create_promise(data)
        print(f"Response from create_promise: {response}")

        return response

    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        return "Hubo un error para encontrar sus datos, lo llamaremos nuevamente brevemente"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Hubo un error para encontrar sus datos, lo llamaremos nuevamente brevemente"

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Hubo un error inesperado: {e}")
