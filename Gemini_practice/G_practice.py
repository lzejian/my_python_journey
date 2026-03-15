raw_orders = [
    {
        "order_id": "ORD-1001",
        "total_amount": 120.50,
        "customer_info": {"country": "US", "is_new_account": False},
        "items": [{"product": "Wireless Mouse", "qty": 1}, {"product": "Keyboard", "qty": 1}]
    },
    {
        "order_id": "ORD-1002",
        "total_amount": 850.00,
        "customer_info": {"country": "NG", "is_new_account": True},
        "items": [{"product": "MacBook Pro", "qty": 1}]
    },
    {
        "order_id": "ORD-1003",
        "total_amount": 45.00,
        "customer_info": {"country": "US", "is_new_account": False},
        "items": [{"product": "Apple Gift Card", "qty": 4}]
    },
    {
        "order_id": "ORD-1004",
        "total_amount": 600.00,
        "customer_info": {"country": "CA", "is_new_account": False},
        "items": [{"product": "Monitor", "qty": 1}, {"product": "Apple Gift Card", "qty": 1}]
    }
]
# A. 核心手撕题（纯手写关键代码）
# 请编写一个函数 filter_risk_orders(orders, amount_threshold, restricted_item)。
# 拦截规则（满足任意一条即判定为高风险）：

# 客户来自非北美地区（非 "US" 且非 "CA"）并且是新账户（is_new_account 为 True）。

# 订单总金额 total_amount 大于或等于 amount_threshold。

# 订单包含特定风控商品（restricted_item），并且该单品的购买数量 qty 大于或等于 3。

# 返回值要求： 返回一个列表（List），里面只包含命中风控规则的 order_id。


def filter_risk_orders(orders, amount_threshold, restricted_item):
    order_id_list = []
    for order in orders:
        if order.get("customer_info",{}).get("country","未知") not in ["US","CA"] and order.get("customer_info",{}).get("is_new_account",False) == True:
            order_id_list.append(order.get("order_id","未知"))
            continue
        elif order.get("total_amount",0) >= amount_threshold:
            order_id_list.append(order.get("order_id","未知"))
            continue
        for item in order.get("items",[]):
            if item.get("product","") == restricted_item and item.get("qty",0) >= 3:
                order_id_list.append(order.get("order_id","未知"))
                break
        else:
            continue
    return order_id_list
risk_orders = filter_risk_orders(raw_orders,500,"Wireless Mouse")
print(risk_orders)

# B.改错
# 昨天有个外包实习生写了下面这段代码，目的是想统计所有购买过 "Apple Gift Card" 的订单总金额。但他被开除了，因为代码不仅有严重的逻辑漏洞，而且跑出来的金额是错的。
# 指出代码中存在的 2个致命错误（不考虑语法报错，只看逻辑和健壮性）：

def calculate_gift_card_revenue(orders):
    revenue = 0
    for order in orders:
        for item in order.get("items",[]):
            if "Apple Gift Card" in item.get("product",""):
                # 累加订单总金额
                revenue = revenue + order.get("total_amount",0)
                break
    return revenue

"""
-------------------------------------------------------------------------
"""

# C. 架构与提示词题（伪代码与防御性编程）
# 在真实的 API 数据源中，由于网络波动或旧版 APP 的问题，有些订单的 customer_info 字典可能是空的，甚至根本没有 customer_info 这个键。
# 你的任务：
# 用 3-4 句话（或伪代码逻辑），向 AI 描述清楚：“在遍历读取 customer_info 里面的 country 字段时，应该如何编写最安全的代码，以防止程序因找不到键值（KeyError）而直接崩溃？”               

# 1.找不到customer_info时，使用.get()方法设置一个空的字典防止出错。
# 2.遍历读取country字段时，也要使用.get()方法设置一个"未知"字符串防止报错。

withdrawals = [
    {
        "req_id": "W-001", 
        "amount": 200, 
        "user_meta": {"kyc_status": "Verified", "region": "EU"}, 
        "bank_tags": ["Traditional", "Local"]
    },
    {
        "req_id": "W-002", 
        "amount": 1500, 
        "user_meta": {"kyc_status": "Pending", "region": "SG"}, 
        "bank_tags": ["Virtual"]
    },
    {
        "req_id": "W-003", 
        "amount": 50, 
        "user_meta": {"kyc_status": "Pending", "region": "US"}, 
        "bank_tags": ["Virtual", "HighRisk"]
    }
]
# 考核任务：
# 请纯手写函数 filter_risky_withdrawals(requests, max_amount)。
# 满足以下任意一条即判定为高风险提现，返回包含 req_id 的列表：

# 用户的 KYC 状态（kyc_status）为 "Pending"，并且其所在地区（region）既不是 "US" 也不是 "UK"。

# 提现金额（amount）大于或等于动态传入的 max_amount。

# 收款银行标签（bank_tags，这是一个列表）中包含 "Virtual" 标签。

# 请吸取刚才的教训，修正全局变量和逻辑运算符的问题。把你的新代码交上来。

def filter_risky_withdrawals(requests, max_amount):
    req_id = []
    for customers in requests:
        if customers.get("user_meta",{}).get("kyc_status","unknown") == "Pending" and customers.get("user_meta",{}).get("region","") not in ["US","UK"]:
            req_id.append(customers.get("req_id","unknown"))
            continue
        if customers.get("amount",0) >= max_amount:
            req_id.append(customers.get("req_id","unknown"))
            continue
        elif "Virtual" in customers.get("bank_tags",[]):
            req_id.append(customers.get("req_id","unknown"))
    return req_id
req_id_list = print(filter_risky_withdrawals(withdrawals, 500))

"""
------------------------------------------------------------------------
"""


raw_orders = {
    "O_101": {"user_id": "U12", "amount": 8000, "items": 2, "country": "NG"},
    "O_102": {"user_id": "U15", "amount": 150,  "items": 1, "country": "US"},
    "O_103": {"user_id": "U22", "amount": 3000, "items": 1, "country": "US"}
}

# 任务 A：核心手撕题】需求说明：
# 请手写一个函数 audit_orders(orders)，接收上述字典作为参数。
# 核心风控逻辑（需严格按顺序判断）：

# 如果订单总金额 (amount) 大于等于 5000，且国家 (country) 是 "NG"，则标记为 "High Risk"，理由是 "Region Alert"。

# 否则，如果单件商品均价（amount 除以 items）大于等于 1000，则标记为 "Medium Risk"，理由是 "High Unit Price"。

# 其他情况均标记为 "Low Risk"，理由是 "Normal"。

# 输出要求：
# 函数最终需要使用 return 返回一个新的字典。新字典的 key 依旧是订单号（如 "O_101"），value 必须是一个包含两个元素的元组：(风险等级, 理由)。

def audit_orders(orders):
    risk_orders_dict = {}
    for order in orders:
        if "_" not in order:
            continue
        try:
            real_box = orders.get(order,{})
            if real_box.get("country","") == "NG" and real_box.get("amount",0) >= 5000:
                risk_orders_dict[order] = ("High Risk","Region Alert")
                continue
            elif real_box.get("amount",0)/real_box.get("items",1) >= 1000:
                risk_orders_dict[order] = ("Medium Risk", "High Unit Price")
                continue
            else:
                risk_orders_dict[order] = ("Low Risk", "Normal")
        except:
            continue
    return risk_orders_dict
risk_dict = audit_orders(raw_orders)
print(risk_dict)



# 【任务 B：验车与 Debug 题】

# 你刚刚完成风控筛选，现在业务线另一个由外包团队（或 AI）写的批量更新数据的函数交到了你手上。这个函数负责把每天新产生的风控结果 new_risk_data 刷入我们的历史数据库 risk_db。

# 业务逻辑要求：

# 如果新数据里有这个订单，更新它。

# 如果新数据里没有，且历史数据库里这个订单是 "Low Risk"，则直接从历史库中删掉它以节省空间。

# 问题代码（包含两个极其致命的初级/中级 Python 漏洞）：

def batch_update_risk(new_risk_data, risk_db={}):
    for order_id in risk_db.keys():
        if order_id in new_risk_data:
            risk_db[order_id] = new_risk_data[order_id]
        else:
            if risk_db[order_id][0] == "Low Risk":
                del risk_db[order_id]
                
    return risk_db

def buy_apple(bag=[]): 
    bag.append("苹果")
    return bag
# 第一次调用，没传参数
result1 = buy_apple()
print(result1)  # 这里会打印出：['苹果']

# 第二次调用，依然没传参数
result2 = buy_apple()
print(result2)