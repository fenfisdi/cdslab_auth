import uvicorn
from fastapi import FastAPI
from routers import user_routers, auth_routers

app = FastAPI()
app.include_router(user_routers.router)
app.include_router(auth_routers.router, tags=["Auth"], prefix="/auth")
