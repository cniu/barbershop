# -*- coding: utf-8 -*-

from sanic import response
from sanic_auth import User

from modules import app, auth

session = {}
@app.middleware('request')
async def add_session_to_request(request):
    request['session'] = session

@app.route('/login', methods=['POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        page_level = request.json.get('page_level', '1')
        login_sql = 'select * from account_list where username = "%s" and password = "%s" and page_level = "%s"' % (username, password, page_level)
        account = await request.app.mysql.query_select(login_sql)
        print()
        if len(account) != 0:
            user = User(account[0][0], username)
            auth.login_user(request, user)
            return response.json({"status": "success"})
    return response.json({"status": "failed"})

@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login.html')

def handle_no_auth(request):
    return response.redirect('/login.html')

@app.route('/api/user')
@auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def api_profile(request, user):
    return response.json(dict(id=user.id, name=user.name))

