from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import router as api_router
import os

app = FastAPI(title="SIIT API - Tesis V1")
if not os.path.exists("static/assets"):
    os.makedirs("static/assets")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router, prefix="/api/v1")

