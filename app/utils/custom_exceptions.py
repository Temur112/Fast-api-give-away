from fastapi import HTTPException, status



def get_user_exception():
    cred = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Validation error Could not validate credientials!",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    return cred

def token_exceptions():
    token_exception_response = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Incorrect email or password",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response

def http_exception():
    return HTTPException(status_code = 404, detail = "item not found")


def custom_response(statuscode = 200, message = "Successful"):
    return {
        'status': statuscode,
        'transaction': message
    }
