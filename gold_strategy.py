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

# ================= 🔧 黄金策略配置区 =================
# 你的 Bark 推送地址 (已帮你填好)
BARK_URL = "https://api.day.app/ZPiQFfbSkpvbGEHvMs8tu5/"
# 汇添富黄金的日定投额
BASE_AMOUNT = 30  
# 黄金专属记账本
DATA_FILE = "gold_strategy_data.json"  
# ====================================================

def send_bark(title, content):
    url = f"{BARK_URL}{title}/{content}"
    try:
        requests.get(url)
    except:
        pass

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    # 默认初始状态
    return {"pool_balance": 0, "last_invest": 0, "consecutive_drop": 0}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

print("🌟 正在启动黄金策略引擎...")
data = load_data()
pool = data['pool_balance']
print(f"💰 当前金库余额: {pool} 元")

try:
    # 1. 获取全球期货数据
    print("正在获取全球黄金行情...")
    df = ak.futures_global_spot_em()
    
    # === 🕵️‍♂️ 核心修复：黄金寻宝逻辑 ===
    # 我们定义一个优先顺序，越靠前的数据越准
    # 1. 伦敦金 (现货，反应最快)
    # 2. 纽约金主 (COMEX主力合约)
    # 3. 包含"纽约黄金"但名字里带"主"的
    
    # 先把 nan 的空值扔掉
    df = df.dropna(subset=['最新价', '涨跌幅'])
    
    # 第一轮筛选：精准打击，找 "伦敦金" (最推荐)
    target = df[df['名称'] == "伦敦金"]
    
    # 第二轮筛选：如果没找到伦敦金，找 "纽约金主"
    if target.empty:
        target = df[df['名称'] == "纽约金主"]
        
    # 第三轮筛选：如果还没找到，找名字里带 "黄金" 且带 "主" 的
    if target.empty:
        mask = df['名称'].str.contains("黄金") & df['名称'].str.contains("主")
        target = df[mask]
        
    # 第四轮筛选（保底）：只要名字带 "纽约黄金" 或 "COMEX黄金"，且不带数字年份（通常主力不带年份）
    if target.empty:
        # 排除掉像 2702 这种带数字的，尽量找纯字母的
        mask = df['名称'].str.contains("纽约黄金|COMEX黄金") & ~df['名称'].str.contains(r"\d", regex=True)
        target = df[mask]

    # === 筛选结束 ===

    if target.empty:
        # 实在找不到，把所有黄金相关的打印出来给你看，方便排查
        all_gold = df[df['名称'].str.contains("黄金")][['名称', '最新价', '涨跌幅']]
        print("❌ 未能自动匹配到主力合约，请查看下方列表：")
        print(all_gold)
        raise Exception("未找到主力黄金数据")

    # 取结果
    name = target['名称'].values[0]
    price = target['最新价'].values[0]
    change_pct = target['涨跌幅'].values[0]
    
    print(f"🥇 锁定合约: {name}")
    print(f"📊 当前价格: {price} (涨跌 {change_pct}%)")

    # ================= 🧠 黄金版策略逻辑 =================
    
    today_invest = 0
    title = ""
    suggestion = ""

    # --- 场景 1: 涨超 0.5% -> 停投 ---
    if change_pct > 0.5:
        title = "🔴金价上涨|暂停定投"
        data['pool_balance'] += BASE_AMOUNT
        data['consecutive_drop'] = 0
        suggestion = f"涨幅 {change_pct}% > 0.5%，今日避高。\n" \
                     f"省下 {BASE_AMOUNT}元 存入金库。\n" \
                     f"💰 当前金库余额: {data['pool_balance']}元"

    # --- 场景 2: 震荡 -0.5% ~ 0.5% -> 正常投 ---
    elif -0.5 <= change_pct <= 0.5:
        title = "🟢金价震荡|正常定投"
        today_invest = BASE_AMOUNT
        data['consecutive_drop'] = 0
        suggestion = f"涨幅 {change_pct}%，波动不大。\n" \
                     f"👉 建议买入: {today_invest} 元"

    # --- 场景 3: 跌超 1.0% -> 黄金坑梭哈 ---
    elif change_pct < -1.0:
        title = "⚡️金价大跌|机会难得"
        # 激进倍数设为 4倍
        today_invest = BASE_AMOUNT * 4 + pool
        data['pool_balance'] = 0
        data['consecutive_drop'] += 1
        suggestion = f"跌幅 {change_pct}% 击穿阈值！\n" \
                     f"🔥 建议买入: {today_invest} 元 (含金库)\n" \
                     f"大跌难得，建议手动确认额度。"

    # --- 场景 4: 小跌 -0.5% ~ -1.0% -> 加仓 ---
    else:
        title = "🟡金价回调|释放库存"
        if data['consecutive_drop'] > 0 and data.get('last_invest', 0) > 0:
            title += "(连跌加码)"
            today_invest = data['last_invest'] * 1.5 
        else:
            today_invest = BASE_AMOUNT + pool
            data['pool_balance'] = 0
            
        data['consecutive_drop'] += 1
        suggestion = f"跌幅 {change_pct}%，触发加仓。\n" \
                     f"👉 建议买入: {today_invest} 元"

    # 保存并推送
    data['last_invest'] = today_invest
    save_data(data)
    print(suggestion)
    send_bark(title, suggestion)

except Exception as e:
    print(f"❌ 出错: {e}")
    send_bark("❌黄金脚本出错", str(e))