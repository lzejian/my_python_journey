import pandas as pd
import numpy as np
import random
from datetime import datetime
import json
import time
import sys

# region agent log
LOG_PATH = "debug-2313ef.log"
RUN_ID = f"run-{int(time.time() * 1000)}"

def debug_log(hypothesis_id, location, message, data):
    payload = {
        "sessionId": "2313ef",
        "runId": RUN_ID,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
# endregion

# region agent log
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
debug_log(
    "H1",
    "test.py:stdout_reconfigure",
    "stdout/stderr encoding reconfigured",
    {
        "stdout_encoding_after": str(getattr(sys.stdout, "encoding", None)),
        "stderr_encoding_after": str(getattr(sys.stderr, "encoding", None)),
    },
)
# endregion

# -------------------------------
# 1. 生成包含恶劣“脏数据”的模拟订单数据
# 说明：这里我们用 pandas 和 numpy 自动生成订单号、客户姓名、购买日期、商品价格、购买数量，并故意制造一些空值、异常格式和不合理数据，模拟真实业务中的脏数据场景
# -------------------------------
num_rows = 100
np.random.seed(42)
debug_log(
    "H1",
    "test.py:init",
    "runtime and encoding snapshot",
    {
        "stdout_encoding": str(getattr(sys.stdout, "encoding", None)),
        "preferred_encoding": str(getattr(sys, "getdefaultencoding", lambda: None)()),
        "num_rows": num_rows,
    },
)

def random_name():
    # 有一定概率插入特殊字符制造异常
    base = ["张三", "李四", "王五", "赵六", "孙七"]
    special = ["@号", "*符号", "#错", "&异常"]
    if random.random() < 0.1:
        return random.choice(base) + random.choice(special)
    elif random.random() < 0.1:
        return "".join(["?" if random.random() < 0.2 else x for x in random.choice(base)])
    else:
        return random.choice(base)

def random_date():
    base_dates = [
        "2023-01-15", "2023/2/8", "2023年3月01日",  # 各种不同格式
        "15-04-2023", "04.18.2023", "2023/13/40",  # 明显不可解析的
        "2022-12-31", "2023-05-09", "2023-06-21"
    ]
    if random.random() < 0.15:
        # 制造一些明显错误的日期
        return random.choice(["2023/99/99", "abcd", None, ""])
    elif random.random() < 0.2:
        return random.choice(base_dates)
    else:
        # 在一定范围内生成正常日期
        return (datetime(2023,1,1) + pd.to_timedelta(random.randint(0, 250), unit="D")).strftime("%Y-%m-%d")

def random_price():
    r = random.random()
    if r < 0.1:
        return None    # 故意空值
    elif r < 0.16:
        return -abs(np.round(np.random.normal(90, 40), 2))  # 负数
    else:
        return np.round(np.random.uniform(20, 2000), 2)

def random_qty():
    r = random.random()
    if r < 0.09:
        return -random.randint(1, 15)   # 负数
    else:
        return random.randint(1, 8)

orders = pd.DataFrame({
    "订单号": ["OD" + str(1000000 + i) for i in range(num_rows)],
    "客户姓名": [random_name() for _ in range(num_rows)],
    "购买日期": [random_date() for _ in range(num_rows)],
    "商品价格": [random_price() for _ in range(num_rows)],
    "购买数量": [random_qty() for _ in range(num_rows)]
})

# -------------------------------
# 2. 脏数据清洗
# 说明：极度防御式逐项判断。价格为空或负数用均值替换；异常日期设为今天；购买数量为负直接删除
# -------------------------------

# 捕获并警告商品价格为空或负的情况
mean_price = orders.loc[orders["商品价格"].apply(lambda x: isinstance(x, (int, float)) and x > 0), "商品价格"].mean()
debug_log(
    "H3",
    "test.py:mean_price",
    "computed mean price for replacements",
    {"mean_price": None if pd.isna(mean_price) else float(mean_price)},
)
def fix_price(row):
    val = row["商品价格"]
    if val is None or not isinstance(val, (int, float)) or val != val:  # 针对 None、NaN
        print(f"警告：订单号{row['订单号']}——商品价格为空，将用均值{mean_price}填充")
        return mean_price
    elif val <= 0:
        print(f"警告：订单号{row['订单号']}——商品价格为负数，将用均值{mean_price}填充")
        return mean_price
    return val

orders["商品价格"] = orders.apply(fix_price, axis=1)

# 统一日期格式，异常日期设为今天，并打印警告
def fix_date(dateval, orderid):
    parsed = None
    try:
        # 先尝试常见显式格式，避免混合格式触发歧义警告
        value = "" if dateval is None else str(dateval).strip()
        if not value:
            raise ValueError("empty date value")
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日", "%d-%m-%Y", "%m.%d.%Y"):
            try:
                parsed = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue
        if parsed is None:
            parsed = pd.to_datetime(value, errors="raise", dayfirst=True).to_pydatetime()
        return parsed.strftime("%Y-%m-%d")
    except Exception:
        today = datetime.today().strftime("%Y-%m-%d")
        print(f"警告：订单号{orderid}——日期格式异常（{dateval}），已设为今日日期{today}")
        return today

orders["购买日期"] = [fix_date(d, oid) for d, oid in zip(orders["购买日期"], orders["订单号"])]
invalid_date_count = int((orders["购买日期"] == datetime.today().strftime("%Y-%m-%d")).sum())
debug_log(
    "H2",
    "test.py:fix_date",
    "date normalization fallback count",
    {"fallback_to_today_count": invalid_date_count},
)

# 删除购买数量为负数的脏数据行
pre_drop = len(orders)
orders = orders[orders["购买数量"] >= 0].copy()
post_drop = len(orders)
if pre_drop > post_drop:
    print(f"共删除了{pre_drop - post_drop}行购买数量为负数的脏数据！")
debug_log(
    "H4",
    "test.py:drop_negative_qty",
    "negative quantity rows dropped",
    {"pre_drop": int(pre_drop), "post_drop": int(post_drop), "dropped": int(pre_drop - post_drop)},
)

# -------------------------------
# 3. 按购买月份分组汇总销售额
# 说明：先提取月份，按月 groupby 计算总售价（价格*数量）
# -------------------------------
orders["购买月份"] = pd.to_datetime(orders["购买日期"]).dt.strftime("%Y-%m")
orders["销售额"] = orders["商品价格"] * orders["购买数量"]
summary = orders.groupby("购买月份", as_index=False)["销售额"].sum().rename(columns={"销售额":"总销售额"})
debug_log(
    "H5",
    "test.py:summary",
    "summary generated",
    {"month_count": int(len(summary)), "total_sales": float(summary["总销售额"].sum())},
)

# -------------------------------
# 4. 导出为 Excel 文件
# 说明：防御性导出，出现异常时打印错误，不崩溃
# -------------------------------
try:
    summary.to_excel("sales_report.xlsx", index=False)
    print("已成功导出销售汇总：sales_report.xlsx")
except Exception as e:
    print(f"导出 Excel 失败！错误信息：{e}")