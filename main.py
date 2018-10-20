# -*- coding: utf-8 -*-

from modules import app, auth
from sanic import response
from modules.sanic_mysql import SanicMysql

from config import db_settings

app.static('/', './web/')

@app.route("/test_api")
async def test(request):
    return response.json({"hello": "world"})

app.config.update(dict(MYSQL=db_settings))
SanicMysql(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)