# -*- coding: utf-8 -*-

from sanic import response
from sanic_auth import User
from sanic.log import logger

from modules import app, auth

@app.route('/login', methods=['POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        page_level = request.json.get('page_level', '1')
        # login_sql = 'select * from users where username = "%s" and password = "%s" and page_level = "%s"' % (username, password, page_level)
        login_sql = 'select * from users where username = "%s" and password = "%s"' % (username, password)
        account = await request.app.mysql.query_select(login_sql)
        if len(account) != 0:
            user = User(account[0][0], username)
            auth.login_user(request, user)
            logger.info("User %s login successfully!" % username)
            return response.json({"message": "Login success!"}, status=200)
    return response.json({"message": "Login failed!"}, status=401)

@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.json({"message": "Logout success."})

def handle_no_auth(request):
    return response.json({"message": "Please login first!"}, status=401)

@app.route('/api/user')
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def api_profile(request, user):
    return response.json(dict(id=user.id, name=user.name))

