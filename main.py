import uvicorn

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

from routers import register_routers, auth_routers


app = FastAPI()

settings = dotenv_values(".env")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings["ALLOWED_HOSTS"]
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings["ALLOWED_ORIGINS"],
    allow_credentials=settings["ALLOW_CREDENTIALS"],
    allow_methods=settings["ALLOWED_METHODS"],
    allow_headers=settings["ALLOWED_HEADERS"]
    )

app.include_router(
    register_routers.router,
    tags=["Register"],
    prefix=settings['REGISTER_PATH']
    )
    
app.include_router(
    auth_routers.router,
    tags=["Auth"],
    prefix=settings['AUTHENTICATION_PATH']
    )
