import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()  # Load environment variables from .env file

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
