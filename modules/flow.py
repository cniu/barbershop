# -*- coding: utf-8 -*-

import uuid, json

from sanic import response
from modules import app, auth
from sanic.views import HTTPMethodView

from modules.authorized import authorized
from modules.login import handle_no_auth

from sanic.log import logger

@app.route("/fellow_money_history", methods=['POST'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getHistory(request):
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

        search_sql = "where CONCAT(IFNULL(`created_time`,''),IFNULL(`phone_number`,''),IFNULL(`sell_item_number`,''),IFNULL(`reason`,'')) LIKE '%%%s%%'" % search

        res_total_count = await request.app.mysql.query_select('select count(*) from fellow_money_history_list %s' % (search_sql))
        total_count = int(res_total_count[0][0])
        if total_count <= (page - 1) * page_size:
            page = 1

        page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
        fellow_money_history_list = await request.app.mysql.query_select('select * from fellow_money_history_list %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
        response_list = []
        for raw_id, value in enumerate(fellow_money_history_list):
            n_id, phone_number, card_type, expend_money, remain_money, sell_item_number, reason, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "phone_number": int(phone_number),
                "card_type": card_type,
                "expend_money": expend_money,
                "remain_money": remain_money,
                "sell_item_number": sell_item_number,
                "reason": reason,
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

@app.route("/employee_money_history", methods=['POST'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getHistory(request):
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

        search_sql = "where CONCAT(IFNULL(`created_time`,''),IFNULL(`phone_number`,''),IFNULL(`sell_item_number`,''),IFNULL(`reason`,'')) LIKE '%%%s%%'" % search

        res_total_count = await request.app.mysql.query_select('select count(*) from employee_money_histroy_list %s' % (search_sql))
        total_count = int(res_total_count[0][0])
        if total_count <= (page - 1) * page_size:
            page = 1

        page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
        employee_money_histroy_list = await request.app.mysql.query_select('select * from employee_money_histroy_list %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
        response_list = []
        for raw_id, value in enumerate(employee_money_histroy_list):
            n_id, phone_number, name, percentage, sell_item_money, money, sell_item_number, reason, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "phone_number": int(phone_number),
                "name": name,
                "percentage": percentage,
                "sell_item_money": int(sell_item_money),
                "money": money,
                "sell_item_number": sell_item_number,
                "reason": reason,
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

@app.route("/cash_flow", methods=['POST'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getHistory(request):
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

        search_sql = "where CONCAT(IFNULL(`created_time`,''),IFNULL(`flow_direction`,''),IFNULL(`sell_item_number`,''),IFNULL(`reason`,'')) LIKE '%%%s%%'" % search

        res_total_count = await request.app.mysql.query_select('select count(*) from cash_flow %s' % (search_sql))
        total_count = int(res_total_count[0][0])
        if total_count <= (page - 1) * page_size:
            page = 1

        page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
        cash_flow = await request.app.mysql.query_select('select * from cash_flow %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
        response_list = []
        for raw_id, value in enumerate(cash_flow):
            n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
            response_list.append({
                "raw_id": raw_id + 1,
                "sell_item_number": sell_item_number,
                "flow_direction": flow_direction,
                "money": money,
                "comment": comment,
                "reason": reason,


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

@app.route("/handle_flow/<flow_type:string>", methods=['POST'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def handleFlow(request, flow_type):
    data = request.json if request.json is not None else {}
    args = request.args if request.args is not None else {}

    logger.info("Cash flow is coming!")
    logger.info("Body is %s" % json.dumps(request.json))

    flow_direction = "in"
    if flow_type == "add_sell_item":
        pass
    elif flow_type == "add_fellow":
        sell_item_number = ""
        flow_direction = "入账"
        money = data.get('money', 0)
        reason = "开卡"
        comment = "会员手机号：%s" % data.get('fellow_phone_number', '')
        sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
            % (sell_item_number, money, flow_direction, reason, comment)
        try:
            logger.debug("New flow SQL: %s" % sql)
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            logger.error("Add fellow flow failed. Reason: %s" % str(e))

    elif flow_type == "add_money_fellow":
        pass
    elif flow_type == "product":
        pass
    elif flow_type == "other":
        pass
    else:
        pass
    return response.json({"status": "success"}) 
    