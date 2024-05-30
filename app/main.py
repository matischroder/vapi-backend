import os
import json
from firebase_admin import credentials, initialize_app
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routes import assistant, call, phone_number


firebase_credentials_path = "app/firebase/serviceAccountKey.json"
cred = credentials.Certificate(firebase_credentials_path)
initialize_app(cred)

app = FastAPI()

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

app.include_router(router)


@app.get("/")
def read_root():
    return {"content": "What are you doing here?", "status_code": 200}
