from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from source.config import settings
from source.db import get_db_connection
from source.routers.authentication import router_of_authentication
from source.routers.register import router_of_registry

app = FastAPI()


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings["ALLOWED_HOSTS"].split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings["ALLOWED_ORIGINS"].split(","),
    allow_methods=settings["ALLOWED_METHODS"].split(","),
    allow_headers=settings["ALLOWED_HEADERS"].split(",")
)

app.include_router(
    router_of_registry,
    tags=["Register"],
    prefix='/register'
)

app.include_router(
    router_of_authentication,
    tags=["Auth"],
    prefix='/login'
)
