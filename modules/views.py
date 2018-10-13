# -*- coding: utf-8 -*-

from sanic import response
from modules import app, auth
from sanic.views import HTTPMethodView

from modules.authorized import authorized
from modules.login import handle_no_auth

class SellItemList(HTTPMethodView):
    decorators = [authorized("main_login")]
    
    async def get(self, request):
        val = await request.app.mysql.query('select * from sell_item_list')
        return response.text(val)

    def post(self, request):
        return response.text('I am post method')

    def put(self, request):
        return response.text('I am put method')

    def patch(self, request):
        return response.text('I am patch method')

    def delete(self, request):
        return response.text('I am delete method')

app.add_route(SellItemList.as_view(), '/sell_items')

@app.route("/")
@auth.login_required(handle_no_auth=handle_no_auth)
async def index(request):
    return response.redirect('/index.html')