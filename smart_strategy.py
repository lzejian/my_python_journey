import akshare as ak
import requests
import json
import os
import pandas as pd
from datetime import datetime  # 👈 确保引入了这个库

# ================= 🛑 周末熔断机制 =================
# 获取今天是周几 (0是周一, 6是周日)
weekday = datetime.now().weekday()

# 如果是周六(5) 或 周日(6)
if weekday > 4:
    print("😴 今天是周末，全球市场休市。")
    print("脚本已自动进入待机模式，不执行任何操作。")
    # 直接终止程序，不再往下跑了
    exit()
# ==================================================

# ================= 🔧 你的私人配置区 (请修改这里) =================
# 1. 你的 Bark 推送链接
BARK_URL = "https://api.day.app/ZPiQFfbSkpvbGEHvMs8tu5/"

# 2. 你的基础日定投额 (比如你纳指每天定投30元)
BASE_AMOUNT = 120 

# 3. 记忆文件的名字 (脚本会自动生成这个文件，不用管)
DATA_FILE = "fund_strategy_data.json"
# ===============================================================

def send_bark(title, content):
    """
    发送 Bark 推送 (Pro版)
    参数说明:
    - isArchive=1: 强制保存历史记录
    - group=基金定投: 消息分组，避免通知栏混乱
    - level=timeSensitive: 时效性通知，确保手表震动
    """
    # 这里的 BARK_URL 结尾通常是 /，所以我们拼接参数时要注意
    # 你的 URL 应该长这样: https://api.day.app/你的key/
    
    # 1. 对内容进行 URL 编码 (防止空格、换行符导致发送失败)
    # 虽然 requests 会自动处理，但为了保险我们用 params 传参
    
    params = {
        "isArchive": "1",           # 🌟 重点：保存历史记录
        "group": "基金定投",         # 🌟 重点：消息分组
        "level": "timeSensitive",   # 🌟 重点：强震动提醒
        # "icon": "https://cdn.icon-icons.com/icons2/1378/PNG/512/chartgraph_92949.png" # (可选) 你甚至可以自定义图标
    }
    
    # 构造完整的请求 URL: base_url + title + / + content
    # 注意：requests 的 get 方法会自动帮我们把 params 拼接到 URL 后面 (?a=1&b=2)
    final_url = f"{BARK_URL}{title}/{content}"
    
    try:
        response = requests.get(final_url, params=params)
        print("✅ 推送已发送 (含归档&分组参数)")
    except Exception as e:
        print(f"❌ 推送失败: {e}")

def load_data():
    """读取'记账本'，看看之前攒了多少钱，昨天干了啥"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    # 如果是第一次运行，或者文件坏了，返回默认初始状态
    return {
        "pool_balance": 0,       # 蓄水池：攒着没投的钱
        "last_action": "init",   # 上一次动作
        "last_invest": 0,        # 上一次投了多少
        "consecutive_drop": 0    # 连续大跌的天数
    }

def save_data(data):
    """把今天的操作记在'记账本'上"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

print("🧠 正在启动智能策略引擎...")
data = load_data()
pool = data['pool_balance']
print(f"💰 当前蓄水池(已攒未投): {pool} 元")

try:
    # 1. 获取行情 (使用我们验证过最稳的接口)
    print("正在获取全球期货数据...")
    df = ak.futures_global_spot_em()
    target = df[df['名称'].str.contains("纳指|纳斯达克", regex=True)]
    
    if target.empty:
        raise Exception("未找到纳指数据")

    # 2. 提取核心指标
    name = target['名称'].values[0]
    price = target['最新价'].values[0]
    change_pct = target['涨跌幅'].values[0]
    
    # 测试用：如果你想强制测试某个涨跌幅，取消下面这行的注释
    # change_pct = -1.0 

    print(f"📊 {name} 当前涨跌: {change_pct}%")
    
    # ================= 🧠 核心策略逻辑 =================
    
    suggestion = ""
    today_invest = 0
    title = ""
    
    # --- 场景 1: 大涨 (> 0.8%) -> 不投，钱攒进池子 ---
    if change_pct > 0.8:
        title = "🔴大涨停投|蓄力模式"
        # 钱存起来
        data['pool_balance'] += BASE_AMOUNT
        data['consecutive_drop'] = 0 # 打断连跌计数
        data['last_action'] = "skip"
        data['last_invest'] = 0
        
        suggestion = f"涨幅 {change_pct}% > 0.8%，今日暂停定投。\n" \
                     f"省下的 {BASE_AMOUNT}元 已存入蓄水池。\n" \
                     f"🏊 当前池子总额: {data['pool_balance']}元"

    # --- 场景 2: 震荡 (-0.8% <= x <= 0.8%) -> 正常投 ---
    elif -0.8 <= change_pct <= 0.8:
        title = "🟢震荡行情|正常定投"
        today_invest = BASE_AMOUNT
        
        # 正常投，池子里的钱不动，连跌清零
        data['consecutive_drop'] = 0
        data['last_action'] = "normal"
        data['last_invest'] = today_invest
        
        suggestion = f"涨幅 {change_pct}%，波动不大。\n" \
                     f"👉 建议买入: {today_invest} 元\n" \
                     f"池子余额 {pool}元 暂不启用。"

    # --- 场景 3: 梭哈 (< -1.5%) -> 满仓干 ---
    elif change_pct < -1.5:
        title = "⚡️暴跌梭哈|捡钱时刻"
        # 这里的“梭哈”逻辑：基础 + 池子全清 + 额外激进倍数(比如5倍)
        # 你可以根据自己财力修改倍数
        today_invest = BASE_AMOUNT * 5 + pool
        
        data['pool_balance'] = 0 # 池子清空
        data['consecutive_drop'] += 1
        data['last_action'] = "all_in"
        data['last_invest'] = today_invest
        
        suggestion = f"暴跌 {change_pct}%！触发熔断级加仓！\n" \
                     f"🔥 建议买入: {today_invest} 元 (含池子库存)\n" \
                     f"机会难得，建议手动检查额度！"

    # --- 场景 4: 大跌 (-1.5% < x < -0.8%) -> 策略加仓 ---
    else:
        # 这里是 -0.8% 到 -1.5% 之间
        title = "🟡大跌加仓|释放库存"
        
        # 逻辑：
        # 如果是“连续下跌”(昨天也跌了)，则加倍昨天的投入
        if data['consecutive_drop'] > 0 and data['last_invest'] > 0:
            title += "(连跌翻倍)"
            # 策略：加倍前一天跌的定投额
            today_invest = data['last_invest'] * 2
            calc_msg = f"触发连跌翻倍 (昨日{data['last_invest']} × 2)"
        else:
            # 如果是“首日下跌”，投入 基础 + 池子里的所有钱
            today_invest = BASE_AMOUNT + pool
            data['pool_balance'] = 0 # 池子清空
            calc_msg = f"基础{BASE_AMOUNT} + 库存{pool}"
            
        data['consecutive_drop'] += 1
        data['last_action'] = "drop_buy"
        data['last_invest'] = today_invest
        
        suggestion = f"跌幅 {change_pct}%，触发加仓策略。\n" \
                     f"👉 建议买入: {today_invest} 元\n" \
                     f"计算公式: {calc_msg}"

    # 保存新的状态
    save_data(data)
    
    # 发送结果
    print(f"策略执行完毕。建议买入: {today_invest}")
    print(suggestion)
    send_bark(title, suggestion)

except Exception as e:
    error_msg = f"策略运行出错: {str(e)}"
    print(error_msg)
    send_bark("❌程序报错", error_msg)