from fastapi import HTTPException


def response_model(data: dict, message: str) -> dict:
    """
        Endpoint response for every successful request

        Parameters
        ----------
        data: dict
            Dictionary containing a successful response
        message: str
            Customized reply

        Returns
        ----------
        Dictionary containing data, a message and a code response
    """

    return {"data": data,
            "code": 200,
            "message": message}


def error_response_model(message, code, error):
    """
        Endpoint response for every failed request

        Parameters
        ----------
        data: dict
            Dictionary containing a failed response
        code: int
            Status code associated with the response
        message: str
            Customized reply

        Returns
        ----------
        Dictionary containing data, a message and a code response
    """
    raise HTTPException(status_code=code,
                        detail=({"error": error,
                                 "code": code,
                                 "message": message, }))
