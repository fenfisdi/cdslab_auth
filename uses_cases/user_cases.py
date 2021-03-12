from operations.user_operations import *
from dependencies import user_deps, qr_deps, responses
from fastapi import HTTPException

def save_user_in_db(user: dict) -> dict:

    if  retrive_user({'email': user.email}):
        raise HTTPException(status_code=404, detail=responses.error_response_model('User already exists', 404, 'Error'))
    else:
        user_in_db = user_deps.transform_props_to_user(user)
        user_insert = insert_user(user_in_db.dict())
        if user_insert:
            url_path = qr_deps.generate_url_qr(user_in_db.key_qr, user)
            return {'email':user_in_db.email, 'url_path': url_path, 'key_qr': user_in_db.key_qr}
        else:
            raise HTTPException(status_code=404, detail=responses.error_response_model('insert error in users collection', 404, 'Error'))
        

def activate_user(user: dict) -> dict:

    is_user = retrive_user({'email': user['email']})

    if is_user:
        is_updated = update_user_state({'is_active': True}, is_user['_id'])

        if is_updated:
            return responses.response_model(is_updated, "successful")
        raise HTTPException(status_code=404, detail=responses.error_response_model("updated error in users collection", 404, "Error"))
    raise HTTPException(status_code=404, detail=responses.error_response_model("user not found", 404, "Error"))

def validate_qr_registration(email: str, qr_value: str) -> bool:

    is_validate = qr_deps.validate_qr({"email": email}, qr_value)
    if is_validate:
        user_deps.send_email(email)
        return "Check your email to finish the registration process"
    raise HTTPException(status_code=404, detail=responses.error_response_model("authorization failure", 404, "Error")) 
