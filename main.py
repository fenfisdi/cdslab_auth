import uvicorn

from dotenv import dotenv_values
from fastapi import FastAPI
from routers import register_routers, auth_routers
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

settings = dotenv_values(".env")
origins = ["*"]

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(register_routers.router, tags=[
                   "Register"], prefix=settings['REGISTER_PATH'])
app.include_router(auth_routers.router, tags=[
                   "Auth"], prefix=settings['AUTHENTICATION_PATH'])
