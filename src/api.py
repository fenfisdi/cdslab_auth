from fastapi import FastAPI

from src.routers import authentication_routes, registry_routes

app = FastAPI()


# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=settings["ALLOWED_HOSTS"].split(",")
# )
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_credentials=False,
#     allow_origins=settings["ALLOWED_ORIGINS"].split(","),
#     allow_methods=settings["ALLOWED_METHODS"].split(","),
#     allow_headers=settings["ALLOWED_HEADERS"].split(",")
# )

app.include_router(
    registry_routes,
    prefix='/register'
)

app.include_router(
    authentication_routes,
    prefix='/login'
)
