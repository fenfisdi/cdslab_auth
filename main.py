import settings
import uvicorn
from fastapi import FastAPI
from routers import user_creation_request

app = FastAPI()
app.include_router(user_creation_request.router)
