import os, time, datetime
import pymysql

db_settings = dict(
	host = '127.0.0.1',
	port = 3306,
	user = 'root',
	password = '*neal_niu_88',
	db = 'barbershop'
)

if __name__ == "__main__":
    now_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")

    if int(now_date.month - 1) / 3 == 0:
        pre_date = datetime.datetime.strptime("%s-07-01" % (now_date.year - 1), "%Y-%m-%d")
        begin_date = datetime.datetime.strptime("%s-10-01" % (now_date.year - 1), "%Y-%m-%d")
        end_date = datetime.datetime.strptime("%s-01-01" % (now_date.year), "%Y-%m-%d")
    elif int(now_date.month - 1) / 3 == 1:
        pre_date = datetime.datetime.strptime("%s-10-01" % (now_date.year - 1), "%Y-%m-%d")
        begin_date = datetime.datetime.strptime("%s-01-01" % (now_date.year), "%Y-%m-%d")
        end_date = datetime.datetime.strptime("%s-04-01" % (now_date.year), "%Y-%m-%d")
    elif int(now_date.month - 1) / 3 == 2:
        pre_date = datetime.datetime.strptime("%s-01-01" % (now_date.year), "%Y-%m-%d")
        begin_date = datetime.datetime.strptime("%s-04-01" % (now_date.year), "%Y-%m-%d")
        end_date = datetime.datetime.strptime("%s-07-01" % (now_date.year), "%Y-%m-%d")
    elif int(now_date.month - 1) / 3 == 3:
        pre_date = datetime.datetime.strptime("%s-04-01" % (now_date.year), "%Y-%m-%d")
        begin_date = datetime.datetime.strptime("%s-07-01" % (now_date.year), "%Y-%m-%d")
        end_date = datetime.datetime.strptime("%s-10-01" % (now_date.year), "%Y-%m-%d")
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd=db_settings['password'], db=db_settings['db'], charset='utf8')
    cursor = conn.cursor()
  
    # 执行SQL，并返回收影响行数
    cursor.execute("select a.*, name from fellow_money_history_list as a, fellow_list as b where a.phone_number = b.phone_number")
    
    fellow_money_history_list = cursor.fetchall()

    fellow_dic = {}
    for raw_id, value in enumerate(fellow_money_history_list):
        n_id, phone_number, card_type, expend_money, remain_money, sell_item_number, reason, created_time, name = value
        if "消费" not in reason:
            continue
        fellow_dic.setdefault(phone_number, {
            "fellow_name": name, 
            "pre_sum_number": 0,
            "current_sum_number": 0,
            "entire_sum_number": 0,
            "entire_items_count": 0,
        })
        if created_time >= begin_date and created_time < end_date:
            fellow_dic[phone_number]["current_sum_number"] += expend_money
        
        if created_time >= pre_date and created_time < begin_date:
            fellow_dic[phone_number]["pre_sum_number"] += expend_money

        fellow_dic[phone_number]["entire_sum_number"] += expend_money
        fellow_dic[phone_number]["entire_items_count"] += 1
    
    result = []
    for phone_number, value in fellow_dic.items():
        current_card_type = ""
        if value["current_sum_number"] >= 500:
            current_card_type = "八折卡"
        if value["current_sum_number"] >= 1000:
            current_card_type = "七折卡"
        if value["current_sum_number"] >= 2000:
            current_card_type = "六折卡"
        if value["current_sum_number"] >= 5000:
            current_card_type = "四折卡"
            
        entire_average_price = 0
        if value["entire_items_count"] != 0:
            entire_average_price = round(value["entire_sum_number"] / value["entire_items_count"], 2)

        result.append((
            phone_number,
            value["fellow_name"],
            value["pre_sum_number"],
            value["current_sum_number"],
            current_card_type,
            value["entire_sum_number"],
            value["entire_items_count"],
            entire_average_price
        ))
    effect_row = cursor.execute("DELETE FROM fellow_analysis_result")
    conn.commit()

    effect_row = cursor.executemany("insert into fellow_analysis_result (phone_number, fellow_name, \
        pre_sum_number, current_sum_number, current_card_type, entire_sum_number, \
        entire_items_count, entire_average_price) values (%s,%s,%s,%s,%s,%s,%s,%s)", 
        result
    )
    print(effect_row)
  
    # 提交，不然无法保存新建或者修改的数据
    conn.commit()
    
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()