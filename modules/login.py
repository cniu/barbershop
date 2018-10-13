# -*- coding: utf-8 -*-

from sanic import response
from modules import app, auth

session = {}
@app.middleware('request')
async def add_session_to_request(request):
    request['session'] = session

@app.route('/login', methods=['POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "chongshangfayi":
            auth.login_user(request, "admin")
            return response.redirect('/index.html')
    return response.redirect('/login.html')

@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login.html')

def handle_no_auth(request):
    return response.redirect('/login.html')

