from fastapi import FastAPI
from router import root_router

fastapi_app = FastAPI()
fastapi_app.include_router(root_router)
