
# 昨天有个外包实习生写了下面这段代码，目的是想统计所有购买过 "Apple Gift Card" 的订单总金额。但他被开除了，因为代码不仅有严重的逻辑漏洞，而且跑出来的金额是错的。
# 指出代码中存在的 2个致命错误（不考虑语法报错，只看逻辑和健壮性）：

def calculate_gift_card_revenue(orders):
    revenue = 0
    for order in orders:
        for item in order.get("items",[]):
            if "Apple Gift Card" in item.get("product",""):
                # 累加订单总金额
                revenue = revenue + order.get("total_amount",0)
    return revenue



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

order_id_list = []
def filter_risk_orders(orders, amount_threshold, restricted_item):
    for order in orders:
        if order.get("customer_info",{}).get["country","未知"] == "US" or "CA" and order.get("is_new_account","") == False:
            order_id_list.append(order.get("order_id",""))
            continue
        elif order.get("total_amount",0) >= amount_threshold:
            order_id_list.append(order.get("order_id",""))
            continue
        