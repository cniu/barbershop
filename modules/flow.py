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
        order_by = args.get('order_key', 'a.created_time')
        order = args.get('order', 'desc')
        if order.lower() not in ['desc', 'asc']:
            order = 'desc'

        search_sql = "where CONCAT(IFNULL(`name`,''),IFNULL(a.`phone_number`,''),IFNULL(`sell_item_number`,''),IFNULL(`reason`,''),IFNULL(a.`created_time`,'')) LIKE '%%%s%%'" % search

        res_total_count = await request.app.mysql.query_select('select count(*) from fellow_money_history_list as a, fellow_list as b %s and a.phone_number = b.phone_number' % (search_sql))
        total_count = int(res_total_count[0][0])
        if total_count <= (page - 1) * page_size:
            page = 1

        page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)
        fellow_money_history_list = await request.app.mysql.query_select('select a.*, name from fellow_money_history_list as a, fellow_list as b %s and a.phone_number = b.phone_number order by %s %s %s' % (search_sql, order_by, order, page_sql))
        response_list = []
        for raw_id, value in enumerate(fellow_money_history_list):
            n_id, phone_number, card_type, expend_money, remain_money, sell_item_number, reason, created_time, name = value
            response_list.append({
                "raw_id": raw_id + 1,
                "phone_number": int(phone_number),
                "name": name,
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

    flow_direction = "入账"
    if flow_type == "add_sell_item":
        hairdresser = data.get('hairdresser', '')
        assistant = data.get('assistant', '')
        sell_money = data.get('money', 0)
        pay_type = data.get('pay_type', "")
        fellow_phone_number = data.get('fellow', '')
        item_number = data.get('item_number', '')

        try:
            if hairdresser != "":
                employee_list = await request.app.mysql.query_select('select percentage, name, phone_number from employee_list where name = "%s"' % hairdresser)
                percentage, name, employee_phone_number = employee_list[0]
                logger.info('Fetch hairdresser information successfully!')

                sql = 'insert into employee_money_histroy_list (phone_number, name, percentage, sell_item_money, money, sell_item_number, reason) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                    % (employee_phone_number, name, percentage, sell_money, int(sell_money) * float(percentage), item_number, "客户消费")
                res = await request.app.mysql.query_other(sql)
                logger.info('Add employee salary history successfully!')

            if assistant != "":
                employee_list = await request.app.mysql.query_select('select percentage, name, phone_number from employee_list where name = "%s"' % assistant)
                percentage, name, employee_phone_number = employee_list[0]
                logger.info('Fetch assistant information successfully!')

                sql = 'insert into employee_money_histroy_list (phone_number, name, percentage, sell_item_money, money, sell_item_number, reason) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                    % (employee_phone_number, name, percentage, sell_money, int(sell_money) * float(percentage), item_number, "客户消费")
                res = await request.app.mysql.query_other(sql)
                logger.info('Add employee salary history successfully!')

            if fellow_phone_number == "":
                reason = "开单"
                flow_direction = "入账"
                comment = "客户消费"
                sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
                    % (item_number, sell_money, flow_direction, reason, comment)
                try:
                    logger.debug("New flow SQL: %s" % sql)
                    res = await request.app.mysql.query_other(sql)
                except Exception as e:
                    logger.error("Add cash flow failed. Reason: %s" % str(e))
            else:
                fellow_list = await request.app.mysql.query_select('select card_type, name, money from fellow_list where phone_number = "%s"' % fellow_phone_number)
                card_type, name, money = fellow_list[0]
                logger.info('Fetch fellow money successfully!')

                if pay_type == "刷卡":
                    sql = 'update fellow_list set money = "%s" where phone_number = "%s"' \
                        % (int(money) - int(sell_money), fellow_phone_number)
                    res = await request.app.mysql.query_other(sql)
                    logger.info('Update fellow money successfully!')

                    sql = 'insert into fellow_money_history_list (phone_number, card_type, expend_money, remain_money, sell_item_number, reason) values ("%s", "%s", "%s", "%s", "%s", "%s")' \
                        % (fellow_phone_number, card_type, sell_money, int(money) - int(sell_money), item_number, "%s消费" % pay_type)
                    res = await request.app.mysql.query_other(sql)
                    logger.info('Add fellow money history successfully!')
                else:
                    sql = 'insert into fellow_money_history_list (phone_number, card_type, expend_money, remain_money, sell_item_number, reason) values ("%s", "%s", "%s", "%s", "%s", "%s")' \
                        % (fellow_phone_number, card_type, sell_money, int(money), item_number, "%s消费" % pay_type)
                    res = await request.app.mysql.query_other(sql)
                    logger.info('Add fellow money history successfully!')


                reason = "开单"
                flow_direction = "不入账"
                if pay_type != "刷卡":
                    flow_direction = "入账"
                comment = "会员%s %s消费" % (fellow_phone_number, pay_type)
                sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
                    % (item_number, sell_money, flow_direction, reason, comment)
                try:
                    logger.debug("New flow SQL: %s" % sql)
                    res = await request.app.mysql.query_other(sql)
                except Exception as e:
                    logger.error("Add cash flow failed. Reason: %s" % str(e))
        except Exception as e:
            logger.error("Add money for fellow failed. Reason: %s" % str(e))
    elif flow_type == "add_fellow":
        fellow_phone_number = data.get('phone_number', '')
        add_money = data.get('money', 0)
        card_type = data.get('card_type', "")
        name = data.get('name', "")
        sell_item_number = ""

        sql = 'insert into fellow_money_history_list (phone_number, card_type, expend_money, remain_money, sell_item_number, reason) values ("%s", "%s", %s, %s, "%s", "%s")' \
            % (fellow_phone_number, card_type, add_money, add_money, "", "开卡")
        res = await request.app.mysql.query_other(sql)
        logger.info('Add fellow money history successfully!')

        flow_direction = "入账"
        reason = "开卡"
        comment = "会员手机号：%s" % fellow_phone_number
        sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
            % (sell_item_number, add_money, flow_direction, reason, comment)
        try:
            logger.debug("New flow SQL: %s" % sql)
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            logger.error("Add fellow flow failed. Reason: %s" % str(e))
    elif flow_type == "add_money_fellow":
        fellow_phone_number = data.get('fellow', '')
        card_type = data.get('card_type', '')
        add_money = data.get('money', 0)
        created_by = data.get('created_by', '')
        flow_direction = "入账"

        try:
            fellow_list = await request.app.mysql.query_select('select name, money from fellow_list where phone_number = "%s"' % fellow_phone_number)
            name, money = fellow_list[0]
            logger.info('Fetch fellow money successfully!')

            sql = 'update fellow_list set card_type = "%s", money = "%s" where phone_number = "%s"' \
                % (card_type, int(add_money) + int(money), fellow_phone_number)
            res = await request.app.mysql.query_other(sql)
            logger.info('Update fellow money successfully!')

            sql = 'insert into fellow_money_history_list (phone_number, card_type, expend_money, remain_money, sell_item_number, reason) values ("%s", "%s", "%s", "%s", "%s", "%s")' \
                % (fellow_phone_number, card_type, add_money, int(add_money) + int(money), "", "充值（操作人：%s）" % created_by)
            res = await request.app.mysql.query_other(sql)
            logger.info('Add fellow money history successfully!')

            reason = "充值"
            comment = "给会员%s充值，操作人：%s" % (fellow_phone_number, created_by)
            sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
                % ("", add_money, flow_direction, reason, comment)
            try:
                logger.debug("New flow SQL: %s" % sql)
                res = await request.app.mysql.query_other(sql)
            except Exception as e:
                logger.error("Add cash flow failed. Reason: %s" % str(e))
        except Exception as e:
            logger.error("Add money for fellow failed. Reason: %s" % str(e))
    elif flow_type == "product_item":
        fellow_phone_number = data.get('fellow', "")
        pay_type = data.get('pay_type', "")
        created_by = data.get('created_by', "")
        item_number = ""
        sell_money = data.get('money', 0)
        reason = "产品消费"
        user_commit = data.get('comment', '')

        if fellow_phone_number == "":
            flow_direction = "入账"
            comment = "操作人：%s（备注：%s）" % (created_by, user_commit)
            sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
                % (item_number, sell_money, flow_direction, reason, comment)
            try:
                logger.debug("New flow SQL: %s" % sql)
                res = await request.app.mysql.query_other(sql)
            except Exception as e:
                logger.error("Add cash flow failed. Reason: %s" % str(e))
        else:
            fellow_list = await request.app.mysql.query_select('select card_type, name, money from fellow_list where phone_number = "%s"' % fellow_phone_number)
            card_type, name, money = fellow_list[0]
            logger.info('Fetch fellow money successfully!')

            sql = 'update fellow_list set money = "%s" where phone_number = "%s"' \
                % (int(money) - int(sell_money), fellow_phone_number)
            res = await request.app.mysql.query_other(sql)
            logger.info('Update fellow money successfully!')

            sql = 'insert into fellow_money_history_list (phone_number, card_type, expend_money, remain_money, sell_item_number, reason) values ("%s", "%s", "%s", "%s", "%s", "%s")' \
                % (fellow_phone_number, card_type, sell_money, int(money) - int(sell_money), item_number, "产品消费")
            res = await request.app.mysql.query_other(sql)
            logger.info('Add fellow money history successfully!')

            flow_direction = "不入账"
            comment = "会员%s产品消费，操作人：%s（备注：%s）" % (fellow_phone_number, created_by, user_commit)
            sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
                % (item_number, sell_money, flow_direction, reason, comment)
            try:
                logger.debug("New flow SQL: %s" % sql)
                res = await request.app.mysql.query_other(sql)
            except Exception as e:
                logger.error("Add cash flow failed. Reason: %s" % str(e))
    elif flow_type == "other_item":
        fellow_phone_number = data.get('fellow', "")
        pay_type = data.get('pay_type', "")
        created_by = data.get('created_by', "")
        item_number = ""
        sell_money = data.get('money', 0)
        reason = "其他消费"
        user_commit = data.get('comment', '')

        if fellow_phone_number == "":
            flow_direction = "入账"
            comment = "操作人：%s（备注：%s, 付款类别：%s）" % (created_by, user_commit, pay_type)
            sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
                % (item_number, sell_money, flow_direction, reason, comment)
            try:
                logger.debug("New flow SQL: %s" % sql)
                res = await request.app.mysql.query_other(sql)
            except Exception as e:
                logger.error("Add cash flow failed. Reason: %s" % str(e))
        else:
            fellow_list = await request.app.mysql.query_select('select card_type, name, money from fellow_list where phone_number = "%s"' % fellow_phone_number)
            card_type, name, money = fellow_list[0]
            logger.info('Fetch fellow money successfully!')

            sql = 'update fellow_list set money = "%s" where phone_number = "%s"' \
                % (int(money) - int(sell_money), fellow_phone_number)
            res = await request.app.mysql.query_other(sql)
            logger.info('Update fellow money successfully!')

            sql = 'insert into fellow_money_history_list (phone_number, card_type, expend_money, remain_money, sell_item_number, reason) values ("%s", "%s", "%s", "%s", "%s", "%s")' \
                % (fellow_phone_number, card_type, sell_money, int(money) - int(sell_money), item_number, "其他消费")
            res = await request.app.mysql.query_other(sql)
            logger.info('Add fellow money history successfully!')

            flow_direction = "不入账"
            comment = "会员%s其他消费，操作人：%s（备注：%s, 付款类别：%s）" % (fellow_phone_number, created_by, user_commit, pay_type)
            sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
                % (item_number, sell_money, flow_direction, reason, comment)
            try:
                logger.debug("New flow SQL: %s" % sql)
                res = await request.app.mysql.query_other(sql)
            except Exception as e:
                logger.error("Add cash flow failed. Reason: %s" % str(e))
    elif flow_type == "single_item":
        flow_direction = data.get('flow_direction', '')
        item_type = data.get('item_type', '')
        money = data.get('money', 0)
        created_by = data.get('created_by', '')
        user_commit = data.get('comment', '')

        reason = item_type
        comment = "操作人：%s（备注：%s）" % (created_by, user_commit)
        sql = 'insert into cash_flow (sell_item_number, money, flow_direction, reason, comment) values ("%s", "%s", "%s", "%s", "%s")' \
            % ("", money, flow_direction, reason, comment)
        try:
            logger.debug("New flow SQL: %s" % sql)
            res = await request.app.mysql.query_other(sql)
        except Exception as e:
            logger.error("Add fellow flow failed. Reason: %s" % str(e))
    else:
        pass
    return response.json({"status": "success"}) 
    