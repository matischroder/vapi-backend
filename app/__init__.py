from fastapi import FastAPI


def create_app():
    app = FastAPI()
    app.include_router(prefix="/")
    return app
