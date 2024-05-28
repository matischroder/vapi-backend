import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    VAPI_API_KEY = os.getenv("VAPI_API_KEY")
    # EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")
    # EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY")
    PORT = os.getenv("PORT")
