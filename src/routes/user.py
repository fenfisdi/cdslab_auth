from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from src.models import UpdateUser
from src.services import UserAPI
from src.use_cases import SecurityUseCase
from src.utils.messages import UserMessage
from src.utils.response import UJSONResponse

user_routes = APIRouter(tags=['User'])


@user_routes.get("/user")
def find_user(user=Depends(SecurityUseCase.validate)):
    email = user.get('email')

    response, is_invalid = UserAPI.find_user(email)
    if is_invalid:
        return response

    data = response.get('data')
    return UJSONResponse(UserMessage.found, HTTP_200_OK, data)


@user_routes.put("/user")
def update_user(
    user_updated: UpdateUser,
    user=Depends(SecurityUseCase.validate)
):
    email = user.get('email')

    response, is_invalid = UserAPI.find_user(email)
    if is_invalid:
        return response

    response, is_invalid = UserAPI.updated_user(
        email,
        user_updated.dict(exclude_none=True)
    )
    if is_invalid:
        return response

    user = response.get("data")
    return UJSONResponse(UserMessage.updated, HTTP_200_OK, user)
