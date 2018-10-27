from sanic import response
from modules import app, auth

from modules.authorized import authorized
from modules.login import handle_no_auth

import json

@app.route("/main_menu")
@auth.login_required(handle_no_auth=handle_no_auth)
async def index(request):
    with open('modules/menu.json', encoding='utf-8') as f:
        menu_list = json.load(f)
    return response.json(menu_list)
