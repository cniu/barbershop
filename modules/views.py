# -*- coding: utf-8 -*-

from sanic import response
from modules import app

from modules.authorized import authorized

@app.route("/login", methods=['GET', 'POST'])
@authorized("main_login")
async def login(request):
	return response.json({"status": "Login Success!"})