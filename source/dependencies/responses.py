from starlette.responses import JSONResponse


def set_json_response(
        message: str,
        code: int = 200,
        data: dict = None
) -> JSONResponse:
    """
        Endpoint response for every successful request

        Parameters
        ----------
        message: str
            Customized reply
        code: int
            Customized reply
        data: dict
            Dictionary containing a successful response


        Returns
        ----------
        Dictionary containing data, a message and a code response
    """
    body = dict(
        message=message,
        code=code,
        data=data,
    )
    return JSONResponse(body, code)
