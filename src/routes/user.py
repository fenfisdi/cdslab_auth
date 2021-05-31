from fastapi import APIRouter, Depends

from src.use_cases import SecurityUseCase

user_routes = APIRouter(tags=['User'])


@user_routes.get("/user")
def find_user(user=Depends(SecurityUseCase.validate)):
    return user
