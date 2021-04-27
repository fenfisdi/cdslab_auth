from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.config import settings
from src.routers import authentication_routes, registry_routes

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.get("ALLOWED_HOSTS", "*").split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=settings.get("ALLOWED_METHODS", "*").split(","),
    allow_headers=settings.get("ALLOWED_HEADERS", "*").split(",")
)

app.include_router(registry_routes)
app.include_router(authentication_routes)
