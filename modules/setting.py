# -*- coding: utf-8 -*-

import uuid

from sanic import response
from modules import app, auth, authorized
from sanic.views import HTTPMethodView

from modules.login import handle_no_auth

class FellowType(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request, item_number):
        data = request.json
        item_list = await request.app.mysql.query_select('select * from fellow_types where id = %s' % item_number)
        response_list = []
        for raw_id, value in enumerate(item_list):
            n_id, card_type_name, discount, comment, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "item_number": str(n_id),
                "card_type_name": card_type_name,
                "discount": discount,
                "comment": comment,
                "created_time": str(created_time),
            })
        return response.json({"data": response_list})

    async def post(self, request, item_number=1):
        data = request.json

        card_type_name = data.get('card_type_name', '')
        discount = data.get('discount', '')
        comment = data.get('comment', '')
        if discount == "":
            discount = 0

        sql = 'insert into fellow_types (card_type_name, discount, comment) values ("%s", "%s", "%s")' \
            % (card_type_name, discount, comment)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "添加卡类型失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "添加卡类型成功"})

    async def put(self, request, item_number):
        data = request.json

        card_type_name = data.get('card_type_name', '')
        discount = data.get('discount', '')
        comment = data.get('comment', '')

        sql = 'update fellow_types set card_type_name = "%s", discount = "%s", comment = "%s" \
            where id = "%s"' \
            % (card_type_name, discount, comment, item_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            print(e)
            return response.json({"status": "failed", "message": "更新失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "更新成功"})

    def patch(self, request):
        return response.text('I am patch method')

    async def delete(self, request, item_number):
        data = request.json

        sql = 'delete from fellow_types where id = "%s"' % (item_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            print(e)
            return response.json({"status": "failed", "message": "更新失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "更新成功"})

app.add_route(FellowType.as_view(), '/setting/fellow_type/<item_number:string>')

class FellowTypes(HTTPMethodView):
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

            search_sql = "where CONCAT(IFNULL(`card_type_name`,''),IFNULL(`discount`,''),IFNULL(`comment`,'')) LIKE '%%%s%%'" % search

            res_total_count = await request.app.mysql.query_select('select count(*) from fellow_types %s' % (search_sql))
            total_count = int(res_total_count[0][0])
            if total_count <= (page - 1) * page_size:
                page = 1

            page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
            fellow_types = await request.app.mysql.query_select('select * from fellow_types %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
            response_list = []
            for raw_id, value in enumerate(fellow_types):
                n_id, card_type_name, discount, comment, created_time = value
                response_list.append({
                    "raw_id": raw_id + 1,
                    "item_number": str(n_id),
                    "card_type_name": card_type_name,
                    "discount": discount,
                    "comment": comment,
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

app.add_route(FellowTypes.as_view(), '/setting/fellow_types/')

class EmployeeType(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth)]

    async def get(self, request, item_number):
        data = request.json
        item_list = await request.app.mysql.query_select('select * from employee_types where id = %s' % item_number)
        response_list = []
        for raw_id, value in enumerate(item_list):
            n_id, type_name, responsibility, comment, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "item_number": str(n_id),
                "type_name": type_name,
                "responsibility": responsibility,
                "comment": comment,
                "created_time": str(created_time),
            })
        return response.json({"data": response_list})

    async def post(self, request, item_number=1):
        data = request.json

        type_name = data.get('type_name', '')
        responsibility = data.get('responsibility', '')
        comment = data.get('comment', '')

        sql = 'insert into employee_types (type_name, responsibility, comment) values ("%s", "%s", "%s")' \
            % (type_name, responsibility, comment)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "添加人员类型失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "添加人员类型成功"})

    async def put(self, request, item_number):
        data = request.json

        type_name = data.get('type_name', '')
        responsibility = data.get('responsibility', '')
        comment = data.get('comment', '')

        sql = 'update employee_types set type_name = "%s", responsibility = "%s", comment = "%s" \
            where id = "%s"' \
            % (type_name, responsibility, comment, item_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            print(e)
            return response.json({"status": "failed", "message": "更新失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "更新成功"})

    def patch(self, request):
        return response.text('I am patch method')

    async def delete(self, request, item_number):
        data = request.json

        sql = 'delete from employee_types where id = "%s"' % (item_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            print(e)
            return response.json({"status": "failed", "message": "更新失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "更新成功"})

app.add_route(EmployeeType.as_view(), '/setting/employee_type/<item_number:string>')

class EmployeeTypes(HTTPMethodView):
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

            search_sql = "where CONCAT(IFNULL(`type_name`,''),IFNULL(`responsibility`,''),IFNULL(`comment`,'')) LIKE '%%%s%%'" % search

            res_total_count = await request.app.mysql.query_select('select count(*) from employee_types %s' % (search_sql))
            total_count = int(res_total_count[0][0])
            if total_count <= (page - 1) * page_size:
                page = 1

            page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
            employee_types = await request.app.mysql.query_select('select * from employee_types %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
            response_list = []
            for raw_id, value in enumerate(employee_types):
                n_id, type_name, responsibility, comment, created_time = value
                response_list.append({
                    "raw_id": raw_id + 1,
                    "item_number": str(n_id),
                    "type_name": type_name,
                    "responsibility": responsibility,
                    "comment": comment,
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

app.add_route(EmployeeTypes.as_view(), '/setting/employee_types/')

class User(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth), authorized.authorized(1)]

    async def get(self, request, item_number):
        data = request.json
        item_list = await request.app.mysql.query_select('select * from users where id = %s' % item_number)
        response_list = []
        for raw_id, value in enumerate(item_list):
            n_id, username, password, page_level, comment, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "item_number": str(n_id),
                "username": username,
                "password": password,
                "page_level": page_level,
                "comment": comment,
                "created_time": str(created_time),
            })
        return response.json({"data": response_list})

    async def post(self, request, item_number=1):
        data = request.json

        username = data.get('username', '')
        password = data.get('password', '')
        page_level = data.get('page_level', 1)
        comment = data.get('comment', '')
        page_level = int(page_level)

        sql = 'insert into users (username, password, page_level, comment) values ("%s", "%s", "%s", "%s")' \
            % (username, password, page_level, comment)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            return response.json({"status": "failed", "message": "添加登陆用户失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "添加登陆用户成功"})

    async def put(self, request, item_number):
        data = request.json

        username = data.get('username', '')
        password = data.get('password', '')
        page_level = data.get('page_level', '')
        comment = data.get('comment', '')

        sql = 'update users set username = "%s", password = "%s", page_level = "%s", comment = "%s" \
            where id = "%s"' \
            % (username, password, page_level, comment, item_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            print(e)
            return response.json({"status": "failed", "message": "更新失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "更新成功"})

    def patch(self, request):
        return response.text('I am patch method')

    async def delete(self, request, item_number):
        data = request.json

        sql = 'delete from users where id = "%s"' % (item_number)
        try:
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            print(e)
            return response.json({"status": "failed", "message": "更新失败，错误信息为%s" % str(e)})

        return response.json({"status": "success", "message": "更新成功"})

app.add_route(User.as_view(), '/setting/user/<item_number:string>')

class Users(HTTPMethodView):
    decorators = [auth.login_required(handle_no_auth=handle_no_auth), authorized.authorized(1)]

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

            search_sql = "where username != 'admin' and CONCAT(IFNULL(`username`,''),IFNULL(`password`,''),IFNULL(`page_level`,''),IFNULL(`comment`,'')) LIKE '%%%s%%'" % search

            res_total_count = await request.app.mysql.query_select('select count(*) from users %s' % (search_sql))
            total_count = int(res_total_count[0][0])
            if total_count <= (page - 1) * page_size:
                page = 1

            page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
            users = await request.app.mysql.query_select('select * from users %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
            response_list = []
            for raw_id, value in enumerate(users):
                n_id, username, password, page_level, comment, created_time = value
                response_list.append({
                    "raw_id": raw_id + 1,
                    "item_number": str(n_id),
                    "username": username,
                    "password": password,
                    "page_level": page_level,
                    "comment": comment,
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

app.add_route(Users.as_view(), '/setting/users/')
