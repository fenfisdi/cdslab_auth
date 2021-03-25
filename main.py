import uvicorn

from dotenv import dotenv_values
from fastapi import FastAPI
from routers import register_routers, auth_routers

settings = dotenv_values(".env")

app = FastAPI()
app.include_router(register_routers.router, tags=["Register"], prefix=settings['REGISTER_PATH'])
app.include_router(auth_routers.router, tags=["Auth"], prefix=settings['AUTHENTICATION_PATH'])
