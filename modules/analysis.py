# -*- coding: utf-8 -*-

import uuid, json, datetime

from sanic import response
from modules import app, auth

from modules.authorized import authorized
from modules.login import handle_no_auth

from sanic.log import logger

@app.route("/get_daily_data/<date_value:string>", methods=['GET'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getData(request, date_value):
    if date_value == "now": date_value = datetime.datetime.today().strftime ('%Y-%m-%d')
    items_count, fellow_item_count, sell_number, sell_money, cost = 0, 0, 0, 0, 0
    sell_money_items_type, sell_item_type = {}, {}
    cash_flow_in_reasons = {}
    summary_sell_money = {}
    hairdresser_sell_number = {}
    assistant_sell_number = {}

    sell_type_list = ['开单', '产品消费', '其他消费']

    week_sell_numbers = {}
    week_sell_money = {}
    sell_item_list = await request.app.mysql.query_select('select * from sell_item_list where to_days(created_time) = to_days("%s")' % date_value)
    for raw_id, value in enumerate(sell_item_list):
        n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment, created_time = value
        if fellow != "":
            fellow_item_count += 1
        items_count += 1
        sell_money_items_type.setdefault(pay_type, {"value": 0, "name": pay_type})["value"] += int(money)
        item_type = ','.join(sorted(item_type.split(',')))
        sell_item_type.setdefault(item_type, {"value": 0, "name": item_type})["value"] += int(money)

        if hairdresser.strip() == "":
            hairdresser_sell_number.setdefault("无发型师", {"value": 0, "name": "无发型师"})["value"] += int(money)
        else:
            hairdresser_sell_number.setdefault(hairdresser, {"value": 0, "name": hairdresser})["value"] += int(money)
        if assistant.strip() == "":
            assistant_sell_number.setdefault("无助理", {"value": 0, "name": "无助理"})["value"] += int(money)
        else:
            assistant_sell_number.setdefault(assistant, {"value": 0, "name": assistant})["value"] += int(money)

    cash_flow = await request.app.mysql.query_select('select * from cash_flow where to_days(created_time) = to_days("%s")' % date_value)
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        if "入账" in flow_direction:
            if reason in sell_type_list:
                sell_number += int(money)
                cash_flow_in_reasons.setdefault(reason, {"value": 0, "name": reason})["value"] += int(money)
            if reason in sell_type_list[1:]:
                hander_person = comment.split('：')[1].split('（')[0]
                if hander_person in hairdresser_sell_number:
                    hairdresser_sell_number.setdefault(hander_person, {"value": 0, "name": hander_person})["value"] += int(money)
                elif hander_person in assistant_sell_number:
                    assistant_sell_number.setdefault(hander_person, {"value": 0, "name": hander_person})["value"] += int(money)

            if flow_direction == "入账":
                sell_money += int(money)
                summary_sell_money.setdefault(reason, {"value": 0, "name": reason})["value"] += int(money)

        if flow_direction == "出账":
            cost += int(money)

    cash_flow = await request.app.mysql.query_select('select * from cash_flow where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(created_time)')
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        created_time = str(created_time)
        week_sell_numbers.setdefault(created_time[0:10], 0)
        week_sell_money.setdefault(created_time[0:10], 0)
        if "入账" in flow_direction:
            if reason in sell_type_list:
                week_sell_numbers[created_time[0:10]] += int(money)
            if flow_direction == "入账":
                week_sell_money[created_time[0:10]] += int(money)

    res = await request.app.mysql.query_select('select count(*) from fellow_money_history_list where reason = "开卡" and to_days(created_time) = to_days("%s")' % date_value)
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
            "cash_flow_in_reasons": list(cash_flow_in_reasons.values()),
            "hairdresser_sell_number": list(hairdresser_sell_number.values()),
            "assistant_sell_number": list(assistant_sell_number.values()),
            "summary_sell_money": list(summary_sell_money.values()),
            "week_sell_numbers": week_sell_numbers,
            "week_sell_money": week_sell_money
        },
        "status": "success"
    })

@app.route("/get_all_data/<date_value:string>", methods=['GET'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getData(request, date_value):
    if date_value == "now": date_value = datetime.datetime.today().strftime ('%Y')
    items_count, fellow_item_count, sell_number, sell_money, cost = 0, 0, 0, 0, 0
    sell_money_items_type, sell_item_type = {}, {}
    cash_flow_in_reasons = {}
    sell_type_list = ['开单', '产品消费', '其他消费']

    year_sell_numbers = {}
    year_sell_money = {}

    if "-" not in date_value:
        temp = 'select * from sell_item_list where YEAR(created_time)="%s"' % date_value
    else:
        temp = 'select * from sell_item_list where YEAR(created_time)="%s" and month(created_time)="%s"' % tuple(date_value.split('-'))

    sell_item_list = await request.app.mysql.query_select(temp)
    for raw_id, value in enumerate(sell_item_list):
        n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment, created_time = value
        if fellow != "":
            fellow_item_count += 1
        items_count += 1
        sell_money_items_type.setdefault(pay_type, {"value": 0, "name": pay_type})["value"] += int(money)
        item_type = ','.join(sorted(item_type.split(',')))
        sell_item_type.setdefault(item_type, {"value": 0, "name": item_type})["value"] += int(money)

    if "-" not in date_value:
        temp = 'select * from cash_flow where YEAR(created_time)="%s"' % date_value
    else:
        temp = 'select * from cash_flow where YEAR(created_time)="%s" and month(created_time)="%s"' % tuple(date_value.split('-'))
    cash_flow = await request.app.mysql.query_select(temp)
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        if "入账" in flow_direction:
            if reason in sell_type_list:
                sell_number += int(money)
                cash_flow_in_reasons.setdefault(reason, {"value": 0, "name": reason})["value"] += int(money)
            if flow_direction == "入账":
                sell_money += int(money)
        if flow_direction == "出账":
            cost += int(money)

    if "-" not in date_value:
        temp = 'select * from cash_flow where YEAR(created_time)="%s"' % date_value
    else:
        temp = 'select * from cash_flow where YEAR(created_time)="%s"' % date_value.split('-')[0]
    cash_flow = await request.app.mysql.query_select(temp)
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        created_time = str(created_time)
        year_sell_numbers.setdefault(created_time[0:7], 0)
        year_sell_money.setdefault(created_time[0:7], 0)
        if "入账" in flow_direction:
            if reason in sell_type_list:
                year_sell_numbers[created_time[0:7]] += int(money)
            if flow_direction == "入账":
                year_sell_money[created_time[0:7]] += int(money)

    if "-" not in date_value:
        temp = 'select * from fellow_money_history_list where reason = "开卡" and YEAR(created_time)="%s"' % date_value
    else:
        temp = 'select * from fellow_money_history_list where reason = "开卡" and YEAR(created_time)="%s" and month(created_time)="%s"' % tuple(date_value.split('-'))
    res = await request.app.mysql.query_select(temp)
    if len(res) == 0:
        new_count_fellow = 0
    else:
        new_count_fellow = res[0][0]

    res = await request.app.mysql.query_select('select count(*), sum(money) FROM barbershop.fellow_list')
    fellow_sum_count, fellow_rest_money = res[0]

    return response.json({
        "data": {
            "new_count_fellow": new_count_fellow,
            "items_count": items_count,
            "fellow_item_count": fellow_item_count,
            "sell_number": sell_number,
            "sell_money": sell_money,
            "cost": cost,
            "fellow_sum_count": fellow_sum_count,
            "fellow_rest_money": fellow_rest_money,
            "sell_money_items_type": list(sell_money_items_type.values()),
            "sell_item_type": list(sell_item_type.values()),
            "year_sell_numbers": year_sell_numbers,
            "year_sell_money": year_sell_money,
            "cash_flow_in_reasons": list(cash_flow_in_reasons.values())
        },
        "status": "success"
    })


@app.route("/get_employee_data/<date_value:string>", methods=['GET'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getData(request, date_value):
    if date_value == "now": date_value = datetime.datetime.today().strftime ('%Y-%m')
    items_count, sell_number = 0, 0
    sell_item_type = {}
    sell_type_list = ['开单']

    employee_analysis_result = {}
    hairdresser_sell_number = {}
    assistant_sell_number = {}
    if "-" not in date_value:
        temp = 'select * from sell_item_list where YEAR(created_time)="%s"' % date_value
    else:
        temp = 'select * from sell_item_list where YEAR(created_time)="%s" and month(created_time)="%s"' % tuple(date_value.split('-'))

    sell_item_list = await request.app.mysql.query_select(temp)
    for raw_id, value in enumerate(sell_item_list):
        n_id, item_number, hairdresser, assistant, item_type, money, pay_type, fellow, comment, created_time = value
        items_count += 1
        item_type = ','.join(sorted(item_type.split(',')))
        sell_item_type.setdefault(item_type, {"value": 0, "name": item_type})["value"] += int(money)

        if hairdresser.strip() == "":
            hairdresser_sell_number.setdefault("无发型师", {"value": 0, "name": "无发型师"})["value"] += int(money)
        else:
            hairdresser_sell_number.setdefault(hairdresser, {"value": 0, "name": hairdresser})["value"] += int(money)
            employee_analysis_result.setdefault(u"发型师：%s 服务类别" % hairdresser, {})
            employee_analysis_result[u"发型师：%s 服务类别" % hairdresser].setdefault(item_type, {"value": 0, "name": item_type})["value"] += int(money)
        if assistant.strip() == "":
            assistant_sell_number.setdefault("无助理", {"value": 0, "name": "无助理"})["value"] += int(money)
        else:
            assistant_sell_number.setdefault(assistant, {"value": 0, "name": assistant})["value"] += int(money)
            employee_analysis_result.setdefault(u"助理：%s 服务类别" % assistant, {})
            employee_analysis_result[u"助理：%s 服务类别" % assistant].setdefault(item_type, {"value": 0, "name": item_type})["value"] += int(money)
        
    if "-" not in date_value:
        temp = 'select * from cash_flow where YEAR(created_time)="%s"' % date_value
    else:
        temp = 'select * from cash_flow where YEAR(created_time)="%s" and month(created_time)="%s"' % tuple(date_value.split('-'))
    cash_flow = await request.app.mysql.query_select(temp)
    for raw_id, value in enumerate(cash_flow):
        n_id, sell_item_number, money, flow_direction, reason, comment, created_time = value
        if "入账" in flow_direction:
            if reason in sell_type_list:
                sell_number += int(money)
    temp_employee_analysis_result = []

    for key, value in employee_analysis_result.items():
        temp_employee_analysis_result.append({"name": key, "content": list(value.values())})
    temp_employee_analysis_result.sort(key = lambda x: x["name"])
    
    return response.json({
        "data": {
            "items_count": items_count,
            "sell_number": sell_number,
            "sell_item_type": list(sell_item_type.values()),
            "hairdresser_sell_number": list(hairdresser_sell_number.values()),
            "assistant_sell_number": list(assistant_sell_number.values()),
            "employee_analysis_result": temp_employee_analysis_result

        },
        "status": "success"
    })

@app.route("/get_fellow_analysis", methods=['POST'])
@auth.login_required(handle_no_auth=handle_no_auth)
async def getData(request):
    try:
        data = request.json if request.json is not None else {}
        args = request.args if request.args is not None else {}

        search = data.get('search', '')
        page = int(args.get('page', 1))
        page_size = int(args.get('page_size', 20))
        order_by = args.get('order_key', 'updated_time')
        order = args.get('order', 'desc')
        if order.lower() not in ['desc', 'asc']:
            order = 'desc'

        search_sql = "where CONCAT(IFNULL(`phone_number`,''),IFNULL(`fellow_name`,''),IFNULL(`updated_time`,'')) LIKE '%%%s%%'" % search

        res_total_count = await request.app.mysql.query_select('select count(*) from fellow_analysis_result %s' % (search_sql))
        total_count = int(res_total_count[0][0])
        if total_count <= (page - 1) * page_size:
            page = 1

        page_sql = "limit %s, %s" % ((page - 1) * page_size, page_size)

        result_list = []
        fellow_analysis_result = await request.app.mysql.query_select('select * from fellow_analysis_result %s order by %s %s %s' % (search_sql, order_by, order, page_sql))
        for raw_id, value in enumerate(fellow_analysis_result):
            n_id, phone_number, fellow_name, pre_sum_number, current_sum_number, current_card_type, entire_sum_number, entire_items_count, entire_average_price, updated_time = value
            fellow_grade = "默认"

            result_list.append({
                "raw_id": raw_id + 1,
                "fellow_name": fellow_name,
                "phone_number": phone_number,
                "pre_sum_number": pre_sum_number,
                "current_sum_number": current_sum_number,
                "current_card_type": current_card_type,
                "entire_sum_number": entire_sum_number,
                "entire_items_count": entire_items_count,
                "entire_average_price": entire_average_price,
                "fellow_grade": fellow_grade,
                "updated_time": str(updated_time),
            })
    except Exception as e:
        return response.json({
            "data": [],
            "page": 1,
            "total_count": 0,
            "status": "failed",
            "message": "获取失败，错误信息为%s" % str(e)
        })

    return response.json({"data": result_list, "page": page, "total_count": int(total_count), "status": "success"})