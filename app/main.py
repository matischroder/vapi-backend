import os
import json
from datetime import datetime
from firebase_admin import credentials, initialize_app
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from app.routes import assistant, call, phone_number, function_calls
from app.models.call import Call
from app.services.dynamo_db.campaigns_service import DynamoDBCampaignService
from app.services.dynamo_db.debts_service import DynamoDBDebtService
from app.services.dynamo_db.assistants_service import DynamoDBAssistantsService
from app.storage import storage

firebase_credentials_path = "app/firebase/serviceAccountKey.json"
cred = credentials.Certificate(firebase_credentials_path)
initialize_app(cred)

campaigns_dynamo_service = DynamoDBCampaignService()
debts_dynamo_service = DynamoDBDebtService()
assistants_dynamo_service = DynamoDBAssistantsService()


async def run_calls():
    now = datetime.now()
    current_hour = now.hour

    all_campaigns = campaigns_dynamo_service.get_all_campaigns()
    current_campaigns = []
    for campaign in all_campaigns:
        if "configuration" in campaign:
            for config in campaign["configuration"]["L"]:
                start_date_str = config["M"]["start_date"]["S"]
                end_date_str = config["M"]["end_date"]["S"]
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                if start_date <= now <= end_date:
                    if "hours_call" in config["M"] and config["M"]["hours_call"]["L"]:
                        hours_call = [
                            int(hour["N"]) for hour in config["M"]["hours_call"]["L"]
                        ]
                        if current_hour in hours_call:
                            current_campaigns.append(campaign)
                            break

    print(current_campaigns)
    for campaign in current_campaigns:
        print(campaign["id"]["S"])
        campaign_id = campaign["id"]["S"]
        debts = debts_dynamo_service.get_debts_by_campaign_id(campaign_id)
        assistant = assistants_dynamo_service.get_assistant(
            campaign["assistant_id"]["S"]
        )
        print(debts)
        print(assistant)
        for debt in debts:
            user_phone = debt["phone"]["SS"][0]
            if not user_phone.startswith("+"):
                user_phone = f"+{user_phone}"  # Agrega el prefijo '+' al número
            new_call = Call(
                debt_id=debt["id"],
                user_phone_number=user_phone,
                project_id=debt["project_id"]["S"],
                campaign_id=debt["campaign_id"]["S"],
                assistant_id=campaign["assistant_id"]["S"],
                company_phone_id=campaign["vapi_phone_id"]["S"],
                debt_amount=debt["amount"]["N"],
                prompt=assistant["prompt"],
                first_message=assistant["first_message"],
            )
            storage.calls[user_phone] = new_call
            await new_call.create_call()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_calls, "interval", minutes=1)
    scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)

cors_origin = os.environ.get("CORS_ORIGIN")
if cors_origin is not None:
    origins = json.loads(cors_origin)
else:
    origins = {}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

router = APIRouter()
router.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])
router.include_router(call.router, prefix="/call", tags=["Calls"])
router.include_router(
    phone_number.router, prefix="/phone_number", tags=["Phone Numbers"]
)
router.include_router(
    function_calls.router, prefix="/function_call", tags=["Function Call"]
)


app.include_router(router)


@app.get("/")
def read_root():
    return {"content": "What are you doing here?", "status_code": 200}
