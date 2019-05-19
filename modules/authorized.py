# -*- coding: utf-8 -*-

from functools import wraps
from sanic.log import logger
from sanic.response import json
from modules import app, auth

def check_request_for_authorization_status(request, page_type):
    current_user = auth.current_user(request)
    if current_user is not None and current_user.level > page_type:
        return True
    return False

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
                return json({'status': 'no_access', 'message': 'please ask for one approve'}, 403)
        return decorated_function
    return decorator

# @app.route("/test_authorized")
# @authorized()
# async def test_author(request):
#     return json({status: 'authorized'})
