from fastapi import FastAPI

from src.routers import authentication_routes, registry_routes

app = FastAPI()

app.include_router(registry_routes)
app.include_router(authentication_routes)
