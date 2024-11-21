from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import STATIC_DIRECTORY
from app.router import routes


app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY), name="static")

app.include_router(routes.router)
