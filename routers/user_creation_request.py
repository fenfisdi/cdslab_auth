from fastapi import HTTPException, APIRouter

from dependencies import user_creation_request
from schemas import user
from db_conection import users

router = APIRouter()

@router.post("/")
async def request_register(user: user.user_create):
    if  users.find_one({'email': user.email}):
        raise HTTPException(status_code=404, detail="User already exists")
    else:
        return user_creation_request.send_registration_email(user.email)

    

    




