from fastapi import HTTPException


def response_model(data: dict, message: str) -> dict:
    """
    Response dict from the endpoint when the request is successful

    Parameters
    ----------
    data: dict
            The dict with the successful response  
    message: str 
            custom message that will be sent as a reply along with data

    Returns
    ----------
    dict with the parameters data, message and the successful response indicator as 200
    """

    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def error_response_model(message, code, error):
    """
    Response dict from the endpoint when the request fails

    Parameters
    ----------
    data: dict
            The dict with the fail response
    code: int
            The status code returned in the response endpoint  
    message: str 
            Custom message that will be sent as a reply along with data

    Returns
    ----------
    dict with the parameters data, code and message
    """
    raise HTTPException(status_code=code, detail=({
        "error": error,
        "code": code,
        "message": message,
    }))
