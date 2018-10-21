# -*- coding: utf-8 -*-

from sanic import Sanic

app = Sanic()

from sanic_auth import Auth

app.config.AUTH_LOGIN_ENDPOINT = 'login'
auth = Auth(app)

from modules import authorized
from modules import views
from modules import login
from modules import exceptions
