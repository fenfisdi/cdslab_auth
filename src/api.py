from os import environ

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.config import fastApiConfig
from src.routes import (
    authentication_routes,
    registry_routes,
    root_routes,
    user_routes
)

app = FastAPI(**fastApiConfig)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=environ.get("ALLOWED_HOSTS", "*").split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=environ.get("ALLOWED_METHODS", "*").split(","),
    allow_headers=environ.get("ALLOWED_HEADERS", "*").split(",")
)

app.include_router(registry_routes)
app.include_router(authentication_routes)
app.include_router(user_routes)
app.include_router(root_routes)
