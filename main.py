import uvicorn
from fastapi import FastAPI
from routers import user_routers

app = FastAPI()
app.include_router(user_routers.router)
