import os
import json
import logging
import datetime
import urllib.parse
import requests

# 引入中国日历库处理法定节假日 (请确保在阿里云 FC 依赖中已安装 chinesecalendar)
try:
    import chinese_calendar
except ImportError:
    pass

# ================= 配置与初始化 =================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger() 
logger.setLevel(logging.INFO)

BARK_TOKEN = os.environ.get("BARK_TOKEN", "")
ALIYUN_APPCODE = os.environ.get("ALIYUN_APPCODE", "") 

API_HEADERS = {
    "Authorization": f"APPCODE {ALIYUN_APPCODE}",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

TARGETS = {
    'sz159501': {'name': '嘉实纳斯达克', 'index': 'NDX', 'futures': 'NQ'},
    'sh513390': {'name': '博时纳斯达克', 'index': 'NDX', 'futures': 'NQ'},
    'sz159660': {'name': '汇添富纳斯达克', 'index': 'NDX', 'futures': 'NQ'},
    'sh513870': {'name': '富国纳斯达克', 'index': 'NDX', 'futures': 'NQ'},
    'sz159696': {'name': '易方达纳斯达克', 'index': 'NDX', 'futures': 'NQ'}
}

STATE_FILE = "/mnt/etf-monitor/qdii_monitor_state.json"

# ================= 状态管理与日历 =================

def is_a_share_trading_day(date_obj):
    """判断今日是否为 A 股交易日"""
    if date_obj.weekday() >= 5:
        return False
    try:
        if chinese_calendar.is_holiday(date_obj):
            return False
    except Exception as e:
        logger.warning(f"⚠️ 日历库缺失或异常，已降级为仅排除周末: {e}")
    return True

def load_state(current_date_str):
    default_state = {
        "date": current_date_str, 
        "dingtou_count": 0,          # 定投每天1次
        "taoli_last_ts": 0.0,        # 30分钟冷却
        "error_count": 0,            # 每天最多2次
        "error_last_ts": 0.0,        # 30分钟冷却
        "morning_report_count": 0,   # 新增：早盘无差别播报，每天1次
        "fund_anchors": {}           # 一基一锚点档案
    }
    if not os.path.exists(STATE_FILE): return default_state
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f: 
            state = json.load(f)
            # 兼容旧版本文件，确保所有键都在
            for k, v in default_state.items():
                if k not in state and k != "date":
                    state[k] = v
        return state if state.get("date") == current_date_str else default_state
    except: return default_state

def save_state(state):
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f: json.dump(state, f)
    except Exception as e: logger.error(f"⚠️ 状态保存失败: {e}")

def get_beijing_time():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

def send_bark(msg):
    if not BARK_TOKEN: return
    try: requests.get(f"https://api.day.app/{BARK_TOKEN}/{urllib.parse.quote(msg)}", timeout=5)
    except: pass

def trigger_error_alert(msg, state, now_obj):
    """服务器抽风特战警报处理器：30分钟CD，每天最多2次"""
    current_ts = now_obj.timestamp()
    if state['error_count'] < 2 and (current_ts - state['error_last_ts'] >= 1800):
        send_bark(f"🚨 系统异常: {msg}")
        state['error_count'] += 1
        state['error_last_ts'] = current_ts
        logger.error(f"🚨 已推送错误警报: {msg}")
        return True
    return False

# ================= 纯 API 业务逻辑 =================

def get_official_navs():
    nav_data, nav_dates = {}, {}
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "http://fundf10.eastmoney.com/"}
    for full_code in TARGETS.keys():
        short_code = full_code[2:]
        url = f"https://api.fund.eastmoney.com/f10/lsjz?fundCode={short_code}&pageIndex=1&pageSize=1"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                lsjz_list = res.json().get("Data", {}).get("LSJZList", [])
                if lsjz_list:
                    nav_data[full_code] = float(lsjz_list[0].get("DWJZ", 0))
                    nav_dates[full_code] = lsjz_list[0].get("FSRQ", "")
        except: pass
    return nav_data, nav_dates

def get_paid_prices_batch(symbols_str):
    url = "https://jmqqgphqcx.market.alicloudapi.com/finance/a-shares-price"
    result = {}
    try:
        res = requests.post(url, headers=API_HEADERS, data={"symbol": symbols_str}, timeout=5)
        if res.status_code == 200:
            data_dict = res.json().get("data", {})
            for sym in symbols_str.split(','):
                item = data_dict.get(sym, {})
                price = float(item.get("price", 0))
                if price > 0:
                    result[sym] = price
    except Exception as e:
        logger.error(f"❌ 场内现价批量API异常: {e}")
    return result

def get_api_realtime_data(asset_type):
    if asset_type == "NQ":
        url = "https://jmqqgphqcx.market.alicloudapi.com/finance/external-futures-price"
        symbol = "NQ"
    else:
        url = "https://jmqqgphqcx.market.alicloudapi.com/finance/foreign-exchange-price"
        symbol = "USDCNH"
        
    try:
        res = requests.post(url, headers=API_HEADERS, data={"symbol": symbol}, timeout=5)
        if res.status_code == 200:
            json_data = res.json()
            if json_data.get("success"):
                data = json_data.get("data")
                if isinstance(data, dict) and symbol in data:
                    data = data[symbol]
                elif isinstance(data, list) and len(data) > 0:
                    data = data[0]
                
                if isinstance(data, dict):
                    price = float(data.get("price", data.get("lastPrice", 0)))
                    if price > 0: return price
    except Exception as e:
        pass
    return None

def get_api_historical_nav_close(asset_type, nav_date_str):
    if asset_type == "NQ":
        url = "https://jmqqgphqcx.market.alicloudapi.com/finance/external-futures-kline"
        symbol = "NQ"
    else:
        url = "https://jmqqgphqcx.market.alicloudapi.com/finance/foreign-exchange-kline"
        symbol = "USDCNH"
        
    try:
        res = requests.post(url, headers=API_HEADERS, data={"symbol": symbol, "type": "0", "limit": "30"}, timeout=8)
        if res.status_code == 200:
            json_data = res.json()
            if not json_data.get("success"): return None
                
            data_node = json_data.get("data", {})
            if isinstance(data_node, dict) and "lines" in data_node and "fields" in data_node:
                lines = data_node.get("lines", [])
                fields = data_node.get("fields", [])
                if not lines: return None
                    
                close_idx = fields.index("close") if "close" in fields else 1
                time_idx = fields.index("tick_at") if "tick_at" in fields else 6 
                
                for k in reversed(lines):
                    ts = int(float(k[time_idx]))
                    dt_bjt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone(datetime.timedelta(hours=8)))
                    dt_trading = dt_bjt - datetime.timedelta(hours=12)
                    k_date = dt_trading.strftime('%Y%m%d')
                    
                    if k_date < nav_date_str.replace("-", ""):
                        logger.info(f"🧩 {asset_type} 成功为基准日 {nav_date_str} 匹配到收盘价: 交易日 {k_date}, 价格 {float(k[close_idx])}")
                        return float(k[close_idx])
    except Exception as e:
        pass
    return None 

# ================= 定投狙击调度引擎 =================

def handler(event, context):
    logger.info("================== 🚀 实盘监控引擎启动 (全天候抗压版) 🚀 ==================")
    now = get_beijing_time()
    current_date_str = now.strftime("%Y-%m-%d")
    current_time = now.time()
    current_ts = now.timestamp()
    
    if not is_a_share_trading_day(now):
        logger.info("⏸️ 今日非 A 股交易日 (周末或法定节假日)，引擎静默待机。")
        return "Non-Trading Day"
        
    # 【午间休市护盾】压缩API调用成本，中午时间段直接退出不扣费
    if datetime.time(11, 30) <= current_time < datetime.time(13, 0):
        logger.info("⏸️ 当前为 A 股午间休市时间，引擎静默待机省钱中。")
        return "Noon Break"
    
    # 【实盘时间轴定义】
    is_dingtou_time = datetime.time(14, 40) <= current_time <= datetime.time(14, 52)
    # 修改：10:00 早盘播报时间 (放宽至 9:55-10:05 兼容触发器时延)
    is_morning_report_time = datetime.time(9, 55) <= current_time <= datetime.time(10, 5)
    # 其余盘中时间均为监控套利时间
    is_taoli_time = not is_dingtou_time and not is_morning_report_time
    
    state = load_state(current_date_str)
    state_updated = False

    logger.info("正在获取各基金官方净值数据...")
    nav_data, nav_dates = get_official_navs()
    if not nav_data:
        state_updated |= trigger_error_alert("东财基金净值接口返回为空，请检查网络！", state, now)
        if state_updated: save_state(state)
        return "Data Error"
    
    logger.info("调用实时 API 获取最新外盘价格...")
    rt_price_nq = get_api_realtime_data("NQ")
    rt_price_usd = get_api_realtime_data("USDCNH")
    if not rt_price_nq or not rt_price_usd:
        state_updated |= trigger_error_alert("阿里云 API 实时外盘数据获取失败，可能触发限流！", state, now)
        if state_updated: save_state(state)
        return "Realtime Error"

    symbols_str = ",".join(TARGETS.keys())
    prices_dict = get_paid_prices_batch(symbols_str)

    # 运行期内存级缓存：防重复扣费
    kline_cache = {}
    results = []

    for code, info in TARGETS.items():
        name = info['name']
        price = prices_dict.get(code)
        nav = nav_data.get(code)
        nav_date = nav_dates.get(code)
        
        if not price or not nav or not nav_date: continue

        # ================= 核心重构：一基一锚点 =================
        anchor = state['fund_anchors'].get(code, {})
        
        if anchor.get("nav_date") != nav_date or not anchor.get("nq_close") or not anchor.get("usd_close"):
            if nav_date not in kline_cache:
                logger.info(f"💡 发现【{name}】的新净值基准日 {nav_date}，请求 K 线 API...")
                nq_c = get_api_historical_nav_close("NQ", nav_date)
                usd_c = get_api_historical_nav_close("USDCNH", nav_date)
                kline_cache[nav_date] = {"nq": nq_c, "usd": usd_c}
            
            closes = kline_cache[nav_date]
            if closes["nq"] and closes["usd"]:
                anchor = {
                    "nav_date": nav_date,
                    "nq_close": closes["nq"],
                    "usd_close": closes["usd"]
                }
                state['fund_anchors'][code] = anchor
                state_updated = True
            else:
                logger.warning(f"⚠️ {name} 历史锚点获取失败，跳过本次计算。")
                state_updated |= trigger_error_alert(f"【{name}】底层K线基准价获取失败，请排查 API！", state, now)
                continue

        mult_nq = rt_price_nq / anchor['nq_close']
        mult_usd = rt_price_usd / anchor['usd_close']

        iopv = nav * mult_nq * mult_usd
        if iopv <= 0: continue
            
        premium = (price - iopv) / iopv * 100
        logger.info(f"🎯 {name} ({code}) -> 现价: {price:.3f}, T-2净值({nav_date}): {nav:.4f}, 估值: {iopv:.4f}, 真实溢价: {premium:.2f}%")
        results.append({'name': name, 'premium': premium, 'price': price})

    if not results: return "Calc Failed"

    # ================= 防神经病安全锁：极差校验 =================
    premiums = [x['premium'] for x in results]
    gap = max(premiums) - min(premiums)
    if gap >= 2.5:
        logger.error(f"🚨 估值极大概率出错！各标的溢价极差达 {gap:.2f}%！")
        state_updated |= trigger_error_alert(f"估值算错啦！同板块基金溢价率相差 {gap:.2f}%，停止定投监控并进行自检！", state, now)
        if state_updated: save_state(state)
        return "Valuation Gap Error"
        
    best_target = min(results, key=lambda x: x['premium'])
    logger.info(f"🏆 当前最优标的: {best_target['name']}，真实溢价率: {best_target['premium']:.2f}%")

    # ================= 交易策略执行 =================
    # 策略 1：非定投时间做 T 套利监控 ( <= -4%, 每30分钟提醒一次 )
    if is_taoli_time and best_target['premium'] <= -4.0:
        if (current_ts - state['taoli_last_ts']) >= 1800:  # 30分钟冷却 (1800秒)
            send_bark(f"⚡ 做T机会！【{best_target['name']}】发生场内踩踏，真实折价达 {best_target['premium']:.2f}%！")
            state['taoli_last_ts'] = current_ts
            state_updated = True
        else:
            logger.info("⌛ 做T机会符合，但处于 30 分钟防骚扰冷却期内。")

    # 策略 2：尾盘精准长线定投 ( <= 2.5%, 每天仅限一次 )
    elif is_dingtou_time and state['dingtou_count'] < 1:
        if best_target['premium'] <= 2.5:
            send_bark(f"🛒 尾盘定投：首选【{best_target['name']}】，真实溢价 {best_target['premium']:.2f}% (符合安全买点)")
            state['dingtou_count'] += 1
            state_updated = True
        else:
            logger.info(f"✋ 暂不推送：最优标的溢价 {best_target['premium']:.2f}%，高于 2.5% 的长线定投基准线。")
            
    # 策略 3：早盘无差别盲报 (每天 10:00 左右限一次，无论溢价高低)
    elif is_morning_report_time and state.get('morning_report_count', 0) < 1:
        send_bark(f"🔔 早盘播报：当前最低【{best_target['name']}】真实溢价 {best_target['premium']:.2f}% (供参考)")
        state['morning_report_count'] = state.get('morning_report_count', 0) + 1
        state_updated = True

    if state_updated: save_state(state)
    logger.info("================== 🏁 监控结束 🏁 ==================")
    return "Success"