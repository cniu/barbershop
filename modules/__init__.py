# -*- coding: utf-8 -*-

from sanic import Sanic

app = Sanic()
app.static('/static', './static')

from modules import authorized
from modules import views