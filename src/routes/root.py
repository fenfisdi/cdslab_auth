from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from src.services import UserAPI
from src.use_cases import SecurityUseCase
from src.utils.messages import UserMessage
from src.utils.response import UJSONResponse

root_routes = APIRouter(prefix='/root', tags=['Root'], include_in_schema=False)


@root_routes.post('/user')
def update_root_user(email: str, admin=Depends(SecurityUseCase.validate_root)):
    response, is_invalid = UserAPI.find_user(email)
    if is_invalid:
        return response

    response, is_invalid = UserAPI.update_root(email)
    if is_invalid:
        return response

    return UJSONResponse(UserMessage.updated, HTTP_200_OK)
