# -*- coding: utf-8 -*-

import uuid, json

from sanic import response
from modules import app, auth

from modules.authorized import authorized
from modules.login import handle_no_auth

from sanic.log import logger

@app.route("/get_daily_data", methods=['GET'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getData(request):
    items_count, fellow_item_count, sell_number, sell_money, cost = 0, 0, 0, 0, 0
    sell_money_items_type, sell_item_type = {}, {}
    cash_flow_in_reasons = {}

    week_sell_numbers = {}

    sell_item_list = await request.app.mysql.query_select('select * from sell_item_list where to_days(created_time) = to_days(now())')
    for raw_id, value in enumerate(sell_item_list):
        n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment, created_time = value
        if fellow != "":
            fellow_item_count += 1
        items_count += 1
        sell_money_items_type.setdefault(pay_type, {"value": 0, "name": pay_type})["value"] += int(money)
        sell_item_type.setdefault(item_type, {"value": 0, "name": item_type})["value"] += int(money)

    cash_flow = await request.app.mysql.query_select('select * from cash_flow where to_days(created_time) = to_days(now())')
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        if "入账" in flow_direction:
            sell_number += int(money)
            cash_flow_in_reasons.setdefault(reason, {"value": 0, "name": reason})["value"] += int(money)
            if flow_direction == "入账":
                sell_money += int(money)
        if flow_direction == "出账":
            cost += int(money)

    cash_flow = await request.app.mysql.query_select('select * from cash_flow where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(created_time)')
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        created_time = str(created_time)
        week_sell_numbers.setdefault(created_time[0:10], 0)
        if "入账" in flow_direction:
            week_sell_numbers[created_time[0:10]] += int(money)

    res = await request.app.mysql.query_select('select count(*) from fellow_money_history_list where reason = "开卡" and to_days(created_time) = to_days(now())')
    new_count_fellow = res[0][0]

    return response.json({
        "data": {
            "new_count_fellow": new_count_fellow,
            "items_count": items_count,
            "fellow_item_count": fellow_item_count,
            "sell_number": sell_number,
            "sell_money": sell_money,
            "cost": cost,
            "sell_money_items_type": list(sell_money_items_type.values()),
            "sell_item_type": list(sell_item_type.values()),
            "week_sell_numbers": week_sell_numbers,
            "cash_flow_in_reasons": list(cash_flow_in_reasons.values())
        },
        "status": "success"
    })

@app.route("/get_all_data", methods=['GET'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getData(request):
    items_count, fellow_item_count, sell_number, sell_money, cost = 0, 0, 0, 0, 0
    sell_money_items_type, sell_item_type = {}, {}
    cash_flow_in_reasons = {}

    year_sell_numbers = {}

    sell_item_list = await request.app.mysql.query_select('select * from sell_item_list where YEAR(created_time)=YEAR(NOW())')
    for raw_id, value in enumerate(sell_item_list):
        n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment, created_time = value
        if fellow != "":
            fellow_item_count += 1
        items_count += 1
        sell_money_items_type.setdefault(pay_type, {"value": 0, "name": pay_type})["value"] += int(money)
        sell_item_type.setdefault(item_type, {"value": 0, "name": item_type})["value"] += int(money)

    cash_flow = await request.app.mysql.query_select('select * from cash_flow where YEAR(created_time)=YEAR(NOW())')
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        if "入账" in flow_direction:
            sell_number += int(money)
            cash_flow_in_reasons.setdefault(reason, {"value": 0, "name": reason})["value"] += int(money)
            if flow_direction == "入账":
                sell_money += int(money)
        if flow_direction == "出账":
            cost += int(money)

    cash_flow = await request.app.mysql.query_select('select * from cash_flow where YEAR(created_time)=YEAR(NOW())')
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        created_time = str(created_time)
        year_sell_numbers.setdefault(created_time[0:7], 0)
        if "入账" in flow_direction:
            year_sell_numbers[created_time[0:7]] += int(money)

    res = await request.app.mysql.query_select('select count(*) from fellow_money_history_list where reason = "开卡" and YEAR(created_time)=YEAR(NOW())')
    new_count_fellow = res[0][0]

    return response.json({
        "data": {
            "new_count_fellow": new_count_fellow,
            "items_count": items_count,
            "fellow_item_count": fellow_item_count,
            "sell_number": sell_number,
            "sell_money": sell_money,
            "cost": cost,
            "sell_money_items_type": list(sell_money_items_type.values()),
            "sell_item_type": list(sell_item_type.values()),
            "year_sell_numbers": year_sell_numbers,
            "cash_flow_in_reasons": list(cash_flow_in_reasons.values())
        },
        "status": "success"
    })
