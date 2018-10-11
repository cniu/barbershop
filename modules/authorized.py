# -*- coding: utf-8 -*-

from functools import wraps
from sanic.response import json

def check_request_for_authorization_status(request, page_type):
    if page_type == "main_login":
        request_data = request.json
        if request_data.get("username", "") == "admin" and request_data.get("password", "") == "chongshangfayi":
            return True
        else:
            return False
    return True

def authorized(page_type):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request, page_type)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized. 
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator

# @app.route("/test_authorized")
# @authorized()
# async def test_author(request):
#     return json({status: 'authorized'})
