# -*- coding: utf-8 -*-

import uuid

from sanic import response
from modules import app, auth
from sanic.views import HTTPMethodView

from modules.authorized import authorized
from modules.login import handle_no_auth

@app.route("/")
# @auth.login_required(handle_no_auth=handle_no_auth)
async def index(request):
    return response.redirect('/web/index.html')


class SellItem(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request, item_number):
        data = request.json
        sell_item_list = await request.app.mysql.query_select('select * from sell_item_list where item_number = %s' % item_number)
        response_list = []
        for raw_id, value in enumerate(sell_item_list):
            n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "item_number": item_number,
                "hairdresser": hairdresser,
                "assistant": assistant,
                "item_type": item_type,
                "money": money,
                "pay_type": pay_type,
                "fellow": fellow,
                "comment": comment,
                "created_time": str(created_time),
            })
        return response.json({"data": response_list})

    async def post(self, request, item_number=1):
        data = request.json

        item_number = str(uuid.uuid4())[:18]
        hairdresser = data.get('hairdresser', '')
        assistant = data.get('assistant', '')
        item_type = data.get('item_type', '')
        money = data.get('money', 0)
        pay_type = data.get('pay_type', '现金')
        fellow = data.get('fellow', '')
        comment = data.get('comment', '')

        sql = 'insert into sell_item_list (item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
            % (item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "开单失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "开单成功"})

    async def put(self, request, item_number):
        data = request.json

        hairdresser = data.get('hairdresser', '')
        assistant = data.get('assistant', '')
        item_type = data.get('item_type', [])
        money = data.get('money', 0)
        pay_type = data.get('pay_type', '现金')
        fellow = data.get('fellow', '')
        comment = data.get('comment', '')

        item_type = ','.join(item_type)
        money = int(money)
        sql = 'update sell_item_list set hairdresser = "%s", assistant = "%s", item_type = "%s", money = "%s", pay_type = "%s", fellow = "%s", comment = "%s" \
            where item_number = "%s"' \
            % (hairdresser, assistant, item_type, money, pay_type, fellow, comment, item_number)
        print(sql)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            print(e)
            return response.json({"status": "failed", "message": "更新失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "更新成功"})

    def patch(self, request):
        return response.text('I am patch method')

    def delete(self, request):
        return response.text('I am delete method')

app.add_route(SellItem.as_view(), '/sell_item/<item_number:string>')


class SellItems(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def post(self, request):
        data = request.json if request.json is not None else {}
        args = request.args if request.args is not None else {}

        try:
            search = data.get('search', '')
            page = int(args.get('page', 1))
            page_size = int(args.get('page_size', 20))
            order_by = args.get('order_key', 'created_time')
            order = args.get('order', 'desc')
            if order.lower() not in ['desc', 'asc']:
                order = 'desc'

            search_sql = "where CONCAT(IFNULL(`item_number`,''),IFNULL(`hairdresser`,''),IFNULL(`assistant`,''),IFNULL(`item_type`,''),IFNULL(`pay_type`,''),IFNULL(`comment`,''),IFNULL(`fellow`,'')) LIKE '%%%s%%'" % search

            res_total_count = await request.app.mysql.query_select('select count(*) from sell_item_list %s' % (search_sql))
            total_count = int(res_total_count[0][0])
            if total_count <= (page - 1) * page_size:
                page = 1

            page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
            sell_item_list = await request.app.mysql.query_select('select * from sell_item_list %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
            response_list = []
            for raw_id, value in enumerate(sell_item_list):
                n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment, created_time = value
                response_list.append({
                    "raw_id": raw_id + 1,
                    "item_number": item_number,
                    "hairdresser": hairdresser,
                    "assistant": assistant,
                    "item_type": item_type,
                    "money": money,
                    "pay_type": pay_type,
                    "fellow": fellow,
                    "comment": comment,
                    "created_time": str(created_time),
                })
        except Exception as e:
            return response.json({
                "data": [],
                "page": 1,
                "total_count": total_count,
                "status": "failed",
                "message": "获取失败，错误信息为%s" % str(e)
            })

        return response.json({"data": response_list, "page": page, "total_count": int(total_count), "status": "success"})

app.add_route(SellItems.as_view(), '/sell_items/')

class Fellows(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def post(self, request):
        data = request.json if request.json is not None else {}
        args = request.args if request.args is not None else {}

        try:
            search = data.get('search', '')
            page = int(args.get('page', 1))
            page_size = int(args.get('page_size', 20))
            order_by = args.get('order_key', 'created_time')
            order = args.get('order', 'desc')
            if order.lower() not in ['desc', 'asc']:
                order = 'desc'

            search_sql = "where CONCAT(IFNULL(`name`,''),IFNULL(`phone_number`,''),IFNULL(`card_type`,''),IFNULL(`created_by`,'')) LIKE '%%%s%%'" % search

            res_total_count = await request.app.mysql.query_select('select count(*) from fellow_list %s' % (search_sql))
            total_count = int(res_total_count[0][0])
            if total_count <= (page - 1) * page_size:
                page = 1

            page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
            fellow_list = await request.app.mysql.query_select('select * from fellow_list %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
            response_list = []
            for raw_id, value in enumerate(fellow_list):
                n_id, name, phone_number, birthday, password, card_type, money, created_by, created_time = value
                response_list.append({
                    "raw_id": raw_id + 1,
                    "name": name,
                    "phone_number": int(phone_number),
                    "birthday": birthday,
                    "card_type": card_type,
                    "money": money,
                    "created_by": created_by,
                    "created_time": str(created_time),
                })
        except Exception as e:
            return response.json({
                "data": [],
                "page": 1,
                "total_count": 0,
                "status": "failed",
                "message": "获取失败，错误信息为%s" % str(e)
            })

        return response.json({"data": response_list, "page": page, "total_count": int(total_count), "status": "success"})

app.add_route(Fellows.as_view(), '/fellows/')

class Fellow(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request, phone_number):
        fellow_list = await request.app.mysql.query_select('select * from fellow_list where phone_number = "%s"' % phone_number)
        response_list = []
        for raw_id, value in enumerate(fellow_list):
            n_id, name, phone_number, birthday, password, card_type, money, created_by, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "name": name,
                "phone_number": phone_number,
                "birthday": birthday,
                "card_type": card_type,
                "money": money,
                "created_by": created_by,
                "created_time": str(created_time),
            })
        return response.json({"data": response_list, "status": "success"})

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
        sql = 'delete from fellow_list where phone_number = "%s"' % s(
            phone_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "删除会员失败，错误信息为%s" % str(e)})
        return response.json({"status": "success", "message": "删除会员成功"})

app.add_route(Fellow.as_view(), '/fellow/<phone_number:int>')


class Employees(HTTPMethodView):
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
        sql = 'delete from fellow_list where phone_number = "%s"' % s(
            phone_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "删除员工失败，错误信息为%s" % str(e)})
        return response.json({"status": "success", "message": "删除员工成功"})

app.add_route(Fellow.as_view(), '/employee/<phone_number:int>')


@app.route("/summarized_employees")
@auth.login_required(handle_no_auth=handle_no_auth)
async def getEmployeesName(request):
    employee_list = await request.app.mysql.query_select('select name, phone_number, emplyee_type from employee_list')
    hairdresser_list, assistant_list, employees = [], [], []
    for raw_id, value in enumerate(employee_list):
        name, phone_number, emplyee_type = value
        if emplyee_type == "发型师":
            hairdresser_list.append({
                "value": name,
                "label": name
            })
        elif emplyee_type == "助理":
            assistant_list.append({
                "value": name,
                "label": name
            })
        employees.append({
                "value": name,
                "label": name
            })
    return response.json({
        "hairdresser_list": hairdresser_list, 
        "assistant_list": assistant_list,
        "employee_list": employees,
        "status": "success"
    })

@app.route("/summarized_fellows")
@auth.login_required(handle_no_auth=handle_no_auth)
async def getFellowsInfo(request):
    employee_list = await request.app.mysql.query_select('select name, phone_number, money, card_type from fellow_list')
    response_list = []
    for raw_id, value in enumerate(employee_list):
        name, phone_number, money, card_type = value
        response_list.append({
            "value": phone_number,
            "label": phone_number,
            "name": name,
            "money": money,
            "card_type": card_type
        })
    return response.json({
        "response_list": response_list,
        "status": "success"
    })

@app.route("/summarized_setting")
@auth.login_required(handle_no_auth=handle_no_auth)
async def getFellowsInfo(request):
    fellow_types = await request.app.mysql.query_select('select card_type_name, comment from fellow_types')
    card_type_list = []
    for raw_id, value in enumerate(fellow_types):
        card_type_name, comment = value
        card_type_list.append({
            "value": card_type_name,
            "label": card_type_name
        })
    return response.json({
        "card_type_list": card_type_list,
        "status": "success"
    })
