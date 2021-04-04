from src.api import app

__all__ = ['app']
from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

from routers.register import router_of_registry
from routers.authentication import router_of_authentication


app = FastAPI()

settings = dotenv_values(".env")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings["ALLOWED_HOSTS"].split(",")
    )

app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings["ALLOW_CREDENTIALS"],
    allow_origins=settings["ALLOWED_ORIGINS"].split(","),
    allow_methods=settings["ALLOWED_METHODS"].split(","),
    allow_headers=settings["ALLOWED_HEADERS"].split(",")
    )

app.include_router(
    router_of_registry,
    tags=["Register"],
    prefix=settings['REGISTER_PATH']
    )

app.include_router(
    router_of_authentication,
    tags=["Auth"],
    prefix=settings['AUTHENTICATION_PATH']
    )
