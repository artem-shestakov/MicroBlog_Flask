from flask import make_response, jsonify, current_app


def response_with(response, headers={}, value=None, message=None):
    """
    Send standard response for request

    :param response: Dict with messae and response code
    :param headers: Response header
    :param value: Additional information about objects
    :param message: Additional text message
    :return: JSON response
    """
    result = {}
    if value is not None:
        result.update(value)
    if response.get('message', None) is not None:
        if message:
            result.update({'message': response['message'] + f'. {message}'})
        else:
            result.update({'message': response['message']})
    result.update({'code': response['code']})
    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'Server': current_app.config['NAME']})
    return make_response(jsonify(result), response['http_code'], headers)