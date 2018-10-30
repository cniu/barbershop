# -*- coding: utf-8 -*-

from sanic import Sanic

app = Sanic()

from sanic_auth import Auth
from sanic_cors import CORS, cross_origin

app.config.AUTH_LOGIN_ENDPOINT = 'login'
app.config['CORS_AUTOMATIC_OPTIONS'] = True

auth = Auth(app)
CORS(app)

from modules import authorized
from modules import views
from modules import login
from modules import exceptions
from modules import front_setting
from modules import setting
