from operations.user_operations import *
from dependencies import user_deps, qr_deps, responses
from fastapi import HTTPException

def send_qr(user: dict) -> dict:

    if  retrive_user({'email': user.email}):
        raise HTTPException(status_code=404, detail=responses.error_response_model('User already exists', 404, 'Error'))
    else:
        user_in_db = user_deps.transform_props_to_user(user)
        user_insert = insert_user(user_in_db.dict())
        if user_insert:
            user_deps.send_email(user)
            url_path = qr_deps.generate_url_qr(user_in_db.key_qr, user)
            return responses.response_model({'url_path': url_path}, "successfull")
        else:
            raise HTTPException(status_code=404, detail=responses.error_response_model('insert error in users collection', 404, 'Error'))
        

def activate_user(user: dict) -> dict:

    is_user = retrive_user({'email': user['email']})

    if is_user:
        is_updated = update_user_state({'is_active': True}, is_user['_id'])

        if is_updated:
            return responses.response_model(is_updated, "successful")
        raise HTTPException(status_code=404, detail=responses.error_response_model("updated error in users collection", 404, "Error"))
    raise HTTPException(status_code=404, detail=responses.error_response_model("user didn´t find", 404, "Error"))




