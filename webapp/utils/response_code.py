"""Standard response message from REST API server"""

SUCCESS_200 = {
    "http_code": 200,
    'code': 'success'
}

SUCCESS_201 = {
    "http_code": 201,
    'code': 'success'
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

UNAUTHORIZED_401 = {
    "http_code": 401,
    "code": "unauthorized",
    "message": "Unauthoried"
}

FORBIDDEN_403 = {
    "http_code": 403,
    "code": "forbidden",
    "message": "Forbidden"
}

NOT_FOUND_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Not found"
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameter",
    "message": "Missing parameters"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}