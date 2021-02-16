import settings
import uvicorn
from fastapi import FastAPI
from routers import user_creation_request

app = FastAPI()
app.include_router(user_creation_request.router)


if __name__ == "__main__":
    uvicorn.run(app, host= settings.host, port= settings.port)
