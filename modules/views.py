# -*- coding: utf-8 -*-

from sanic import response
from modules import app, auth
from sanic.views import HTTPMethodView

from modules.authorized import authorized
from modules.login import handle_no_auth


@app.route("/")
# @auth.login_required(handle_no_auth=handle_no_auth)
async def index(request):
    return response.redirect('/index.html')

class SellItem(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request):
        sell_item_list = await request.app.mysql.query_select('select * from sell_item_list')
        response_list = []
        for raw_id, value in enumerate(sell_item_list):
            n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, update_time = value
            response_list.append([
                raw_id,
                item_number, hairdresser, assistant, item_type, money, pay_type, fellow, str(
                    update_time)
            ])
        return response.json({"data": response_list})

    def post(self, request):
        return response.text('I am post method')

    def put(self, request):
        return response.text('I am put method')

    def patch(self, request):
        return response.text('I am patch method')

    def delete(self, request):
        return response.text('I am delete method')

app.add_route(SellItem.as_view(), '/sell_items')

class Fellows(HTTPMethodView):
    # decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request):
        fellow_list = await request.app.mysql.query_select('select * from fellow_list')
        response_list = []
        for raw_id, value in enumerate(fellow_list):
            n_id, name, phone_number, birthday, password, card_type, money, created_by, update_time = value
            response_list.append([
                raw_id,
                name, phone_number, birthday, password, card_type, money, created_by, str(
                    update_time)
            ])
        return response.json({"data": response_list})

app.add_route(Fellows.as_view(), '/fellows/')

class Fellow(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request, phone_number):
        fellow_list = await request.app.mysql.query_select('select * from fellow_list where phone_number = "%s"' % phone_number)
        response_list = []
        for raw_id, value in enumerate(fellow_list):
            n_id, name, phone_number, birthday, password, card_type, money, created_by, update_time = value
            response_list.append([
                raw_id,
                name, phone_number, birthday, password, card_type, money, created_by, str(
                    update_time)
            ])
        return response.json({"data": response_list})

    async def post(self, request, phone_number):
        data = request.json
        name, phone_number, birthday, password, card_type, money, created_by = (
            data.get('name', ''),
            data.get('phone_number', phone_number),
            data.get('birthday', ''),
            data.get('password', ''),
            data.get('card_type', ''),
            data.get('money', 0),
            data.get('created_by', '')
        )
        sql = 'insert into fellow_list (name, phone_number, birthday, password, card_type, money, created_by) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
            % (name, phone_number, birthday, password, card_type, money, created_by)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "开卡失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "开卡成功"})

    async def put(self, request, phone_number):
        data = request.json
        name, birthday, password, card_type, money, created_by = (
            data.get('name', ''),
            data.get('birthday', ''),
            data.get('password', ''),
            data.get('card_type', ''),
            data.get('money', 0),
            data.get('created_by', '')
        )
        sql = 'update fellow_list (name, birthday, password, card_type, money, created_by) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s") where phone_number = "%s"' \
            % (name, birthday, password, card_type, money, created_by, phone_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": str(e)})
        return response.json({"status": "success", "message": "更新会员信息成功"})

    async def delete(self, request, phone_number):
        data = request.json
        sql = 'delete from fellow_list where phone_number = "%s"' %s (phone_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "删除会员失败，错误信息为%s" % str(e)})
        return response.json({"status": "success", "message": "删除会员成功"})

app.add_route(Fellow.as_view(), '/fellow/<phone_number:int>')

class Fellows(HTTPMethodView):
    # decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request):
        employee_list = await request.app.mysql.query_select('select * from employee_list')
        response_list = []
        for raw_id, value in enumerate(employee_list):
            n_id, name, phone_number, birthday, emplyee_type, base_salary, percentage, status, update_time = value
            response_list.append([
                raw_id,
                name, phone_number, birthday, emplyee_type, base_salary, percentage, status, str(
                    update_time)
            ])
        return response.json({"data": response_list})

app.add_route(Fellows.as_view(), '/emplyees/')

class Employee(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request, phone_number):
        employee_list = await request.app.mysql.query_select('select * from employee_list where phone_number = "%s"' % phone_number)
        response_list = []
        for raw_id, value in enumerate(employee_list):
            n_id, name, phone_number, birthday, emplyee_type, base_salary, percentage, status, update_time = value
            response_list.append([
                raw_id,
                name, phone_number, birthday, emplyee_type, base_salary, percentage, status, str(
                    update_time)
            ])
        return response.json({"data": response_list})

    async def post(self, request, phone_number):
        data = request.json
        name, phone_number, birthday, emplyee_type, base_salary, percentage, status = (
            data.get('name', ''),
            data.get('phone_number', phone_number),
            data.get('birthday', ''),
            data.get('emplyee_type', ''),
            data.get('base_salary', ''),
            data.get('percentage', 0),
            data.get('status', 0)
        )
        sql = 'insert into employee_list (name, phone_number, birthday, emplyee_type, base_salary, percentage, status) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
            % (name, phone_number, birthday, emplyee_type, base_salary, percentage, status)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "增加员工失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "成功增加一位员工！"})

    async def put(self, request, phone_number):
        data = request.json
        name, birthday, password, card_type, money, created_by = (
            data.get('name', ''),
            data.get('phone_number', phone_number),
            data.get('birthday', ''),
            data.get('emplyee_type', ''),
            data.get('base_salary', ''),
            data.get('percentage', 0),
            data.get('status', 0)
        )
        sql = 'update fellow_list (name, phone_number, birthday, emplyee_type, base_salary, percentage, status) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s") where phone_number = "%s"' \
            % (name, phone_number, birthday, emplyee_type, base_salary, percentage, status)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": str(e)})
        return response.json({"status": "success", "message": "更新员工信息成功"})

    async def delete(self, request, phone_number):
        data = request.json
        sql = 'delete from fellow_list where phone_number = "%s"' %s (phone_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "删除员工失败，错误信息为%s" % str(e)})
        return response.json({"status": "success", "message": "删除员工成功"})

app.add_route(Fellow.as_view(), '/employee/<phone_number:int>')