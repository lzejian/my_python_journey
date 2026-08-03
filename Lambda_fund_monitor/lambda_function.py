"""
AWS Lambda / Docker 容器 - 统一每日监控系统 (v3.3 终极修复版)
====================================================================
模块 A：TQQQ 四维量化状态机（State Machine）风控策略
模块 B：QDII 基金公告监控（仅保留景顺长城全球半导体芯片）

版本 v3.3 核心修复:
  - 修复 compute_net_liquidity_change 中未对元组取 [1] 索引导致的 TypeError 减法错误
  - 维持 VIX POST API 自动展期换月 (VX2608 / VX2609)
  - 维持四维量化状态机 (RED / ORANGE / YELLOW / GREEN) 逻辑

环境要求：
  Python 3.10+
  依赖库: boto3, yfinance, pandas, pandas_ta, requests

环境变量：
  - BARK_TOKEN: Bark 推送 Token
  - FRED_API_KEY: FRED API 密钥
  - ALIYUN_APPCODE: 阿里云市场 AppCode
  - S3_BUCKET: 存储 QDII 历史记录的 S3 桶名 (非 S3 环境留空即可)
  - S3_STATE_KEY: S3 状态文件 Key
"""

import json
import os
import logging
import time
from datetime import datetime, timedelta

import boto3
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests

# ============================================================
# 全局配置
# ============================================================
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

BARK_TOKEN = os.environ.get("BARK_TOKEN", "WWBFmjRYERrAUBDRskK3Gn")
BARK_BASE_URL = f"https://api.day.app/{BARK_TOKEN}/"

FRED_API_KEY = os.environ.get("FRED_API_KEY", "749812e69e99644cfd562b14b57461aa")
FRED_SAHM = "SAHMREALTIME"          # 萨姆规则实时指标
FRED_HY_OAS = "BAMLH0A0HYM2"        # 高收益信用利差 (OAS)
FRED_T10Y2Y = "T10Y2Y"              # 10Y-2Y 美债利差
FRED_WALCL = "WALCL"                # 美联储总资产
FRED_WTREGEN = "WTREGEN"            # 财政部一般账户 (TGA)
FRED_RRPONTSYD = "RRPONTSYD"        # 隔夜逆回购

ALIYUN_APPCODE = os.environ.get("ALIYUN_APPCODE", "cad000d1ad8a4b35a17a5825a9b3d4ab")
VIX_API_URL = os.environ.get("VIX_API_URL", "https://lhgphqcx.market.alicloudapi.com/finance/external-futures-price")

SMA_PERIOD = 200
ATR_PERIOD = 14
ADX_PERIOD = 14
ATR_MULTIPLIER = 2.0                # 动态止损乘数
ADX_MONKEY_THRESHOLD = 20           # ADX < 20 判定为猴市
LOOKBACK_DAYS = 300

SAHM_THRESHOLD = 0.50               # 萨姆规则衰退阈值 (%)
HY_OAS_THRESHOLD = 5.50             # 高收益利差警戒线 (%)
NET_LIQUIDITY_DROP_THRESHOLD = -8.0  # 净流动性3月跌幅阈值 (%)
VIX_BACKWARDATION_THRESHOLD = 1.0   # VIX 期货贴水阈值 (VIX1/VIX2 > 1.0)

QDII_API_URL = "https://lhjjhqsjcx.market.alicloudapi.com/fund/notice"
S3_BUCKET = os.environ.get("S3_BUCKET", "")
S3_STATE_KEY = os.environ.get("S3_STATE_KEY", "fund_notice_state_v2.json")

CUTOFF_DATETIME = datetime.now() - timedelta(days=30)
CUTOFF_DATE_STR = CUTOFF_DATETIME.strftime("%Y-%m-%d %H:%M:%S")

QDII_FUNDS = {
    "501225": "景顺长城全球半导体芯片股票A",
}

s3_client = boto3.client("s3") if S3_BUCKET else None


# ============================================================
# 公共工具函数
# ============================================================
def send_bark(title: str, body: str, group: str = "量化监控") -> bool:
    """通过 Bark API 推送消息到手机"""
    try:
        payload = {"title": title, "body": body, "group": group}
        resp = requests.post(BARK_BASE_URL, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f"Bark 推送成功: [{group}] {title}")
        return True
    except Exception as e:
        logger.error(f"Bark 推送失败: {e}")
        return False


def get_yfinance_data_with_retry(ticker_symbol: str, period: str, max_retries: int = 3) -> pd.DataFrame:
    """带重试机制的 yfinance 数据获取函数"""
    for attempt in range(1, max_retries + 1):
        try:
            ticker = yf.Ticker(ticker_symbol)
            df = ticker.history(period=period)
            if not df.empty:
                return df
            logger.warning(f"第 {attempt} 次尝试获取 {ticker_symbol} 数据为空。")
        except Exception as e:
            logger.warning(f"第 {attempt} 次尝试获取 {ticker_symbol} 数据失败: {e}")

        if attempt < max_retries:
            time.sleep(3)

    return pd.DataFrame()


def get_fred_series_latest(series_id: str, max_retries: int = 3) -> float | None:
    """从 FRED API 获取指定序列的最新数值（带重试降级）"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 10,
    }
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            observations = resp.json().get("observations", [])
            for obs in observations:
                value = obs.get("value", ".")
                if value != ".":
                    return float(value)
            return None
        except Exception as e:
            logger.warning(f"FRED {series_id} 第 {attempt} 次请求失败: {e}")
            if attempt < max_retries:
                time.sleep(3)

    logger.error(f"FRED {series_id} 全部 {max_retries} 次重试失败，降级处理")
    return None


def get_fred_series_history(series_id: str, observation_start: str, max_retries: int = 3) -> list:
    """从 FRED API 获取指定序列的历史数据（用于计算变动率）"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": observation_start,
        "sort_order": "asc",
    }
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            observations = resp.json().get("observations", [])
            return [(obs["date"], float(obs["value"])) for obs in observations if obs.get("value", ".") != "."]
        except Exception as e:
            logger.warning(f"FRED {series_id} history 第 {attempt} 次请求失败: {e}")
            if attempt < max_retries:
                time.sleep(3)

    logger.error(f"FRED {series_id} history 全部重试失败")
    return []


# ============================================================
# VIX 期货新接口 (POST) 与自动展期/换月逻辑
# ============================================================
def get_vix_contract_symbols(now: datetime = None) -> tuple[str, str]:
    """
    动态计算近月(VIX1)和远月(VIX2)合约代码（格式: VX2608, VX2609）。
    每月 18 号之后自动换月进下一个月合约，绝不使用过期旧合约。
    """
    if now is None:
        now = datetime.now()

    if now.day > 18:
        if now.month == 12:
            m1_year, m1_month = now.year + 1, 1
        else:
            m1_year, m1_month = now.year, now.month + 1
    else:
        m1_year, m1_month = now.year, now.month

    if m1_month == 12:
        m2_year, m2_month = m1_year + 1, 1
    else:
        m2_year, m2_month = m1_year, m1_month + 1

    vix1_symbol = f"VX{m1_year % 100:02d}{m1_month:02d}"
    vix2_symbol = f"VX{m2_year % 100:02d}{m2_month:02d}"

    return vix1_symbol, vix2_symbol


def fetch_vix_contract_price(symbol: str) -> float | None:
    """调用新版外盘期货报价接口 (POST) 获取最新现价"""
    headers = {
        "Authorization": f"APPCODE {ALIYUN_APPCODE}",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    payload = {
        "symbol": symbol,
    }

    try:
        resp = requests.post(VIX_API_URL, headers=headers, data=payload, timeout=10)
        if resp.status_code != 200:
            logger.warning(f"[VIX API] 查询 {symbol} 失败, HTTP 状态码: {resp.status_code}")
            return None

        res_json = resp.json()
        logger.info(f"[VIX API] {symbol} 返回数据: {res_json}")

        if res_json.get("code") == 200 or res_json.get("success") is True:
            data = res_json.get("data", {})
            if isinstance(data, dict) and "price" in data:
                return float(data["price"])

        return None
    except Exception as e:
        logger.error(f"[VIX API] 查询 {symbol} 异常: {e}")
        return None


def get_vix_futures_ratio() -> float | None:
    """
    计算 VIX 期货近月与远月比值 (VIX1 / VIX2)
    比值 > 1.0 表示 Backwardation（贴水/恐慌）
    """
    vix1_sym, vix2_sym = get_vix_contract_symbols()
    logger.info(f"[VIX] 动态计算合约代码: 近月={vix1_sym}, 远月={vix2_sym}")

    p1 = fetch_vix_contract_price(vix1_sym)
    p2 = fetch_vix_contract_price(vix2_sym)

    if p1 is not None and p2 is not None and p2 > 0:
        ratio = round(p1 / p2, 4)
        logger.info(f"[VIX] 获取成功: {vix1_sym}={p1}, {vix2_sym}={p2}, 比值={ratio}")
        return ratio
    else:
        logger.warning(f"[VIX] 获取价格失败: {vix1_sym}={p1}, {vix2_sym}={p2}")
        return None


# ============================================================
# 模块 A：四维量化状态机
# ============================================================
def compute_net_liquidity_change() -> float | None:
    """
    计算美联储净流动性 3 个月变动率 (%)
    Net Liquidity = WALCL - WTREGEN - RRPONTSYD
    """
    start_date = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")

    walcl_data = get_fred_series_history(FRED_WALCL, start_date)
    tga_data = get_fred_series_history(FRED_WTREGEN, start_date)
    rrp_data = get_fred_series_history(FRED_RRPONTSYD, start_date)

    if not walcl_data or not tga_data or not rrp_data:
        logger.warning("[流动性] 部分 FRED 数据不可用，无法计算净流动性")
        return None

    # 修复：加上索引 [1]，提取元组 ('2026-07-31', 7500000.0) 中的浮点数值
    walcl_latest = walcl_data[-1][1]
    tga_latest = tga_data[-1][1]
    rrp_latest = rrp_data[-1][1]
    net_latest = walcl_latest - tga_latest - rrp_latest

    walcl_old = walcl_data[0][1]
    tga_old = tga_data[0][1]
    rrp_old = rrp_data[0][1]
    net_old = walcl_old - tga_old - rrp_old

    if net_old == 0:
        return None

    change_pct = ((net_latest - net_old) / abs(net_old)) * 100
    return round(change_pct, 2)


def run_state_machine() -> tuple[str, str]:
    """
    执行四维量化状态机分析
    返回: (完整报告文本, 状态等级 RED/ORANGE/YELLOW/GREEN)
    """
    logger.info("[状态机] 正在获取 QQQ 技术面数据...")

    df = get_yfinance_data_with_retry("QQQ", period=f"{LOOKBACK_DAYS}d")

    if df.empty or len(df) < SMA_PERIOD:
        raise ValueError(f"QQQ 数据获取失败或不足: 仅获取 {len(df)} 条，需要至少 {SMA_PERIOD} 条")

    latest_date = df.index[-1]
    if isinstance(latest_date, pd.Timestamp) and latest_date.tzinfo:
        latest_date = latest_date.tz_localize(None)

    close = df["Close"].iloc[-1]
    sma200 = df["Close"].rolling(window=SMA_PERIOD).mean().iloc[-1]
    atr_series = ta.atr(df["High"], df["Low"], df["Close"], length=ATR_PERIOD)
    atr14 = atr_series.iloc[-1]
    adx_series = ta.adx(df["High"], df["Low"], df["Close"], length=ADX_PERIOD)
    adx14 = adx_series[f"ADX_{ADX_PERIOD}"].iloc[-1]

    # 动态止损线
    stop_level = sma200 - (ATR_MULTIPLIER * atr14)

    logger.info("[状态机] 正在获取 FRED 宏观面数据...")
    sahm_value = get_fred_series_latest(FRED_SAHM)
    hy_oas = get_fred_series_latest(FRED_HY_OAS)
    t10y2y = get_fred_series_latest(FRED_T10Y2Y)
    net_liq_change = compute_net_liquidity_change()

    logger.info("[状态机] 正在获取 VIX 期货数据...")
    vix_ratio = get_vix_futures_ratio()

    # 状态判定逻辑
    state = "GREEN"
    state_reason = ""

    red_triggers = []
    if sahm_value is not None and sahm_value >= SAHM_THRESHOLD:
        red_triggers.append(f"萨姆规则 {sahm_value:.2f}% >= {SAHM_THRESHOLD}%")
    if hy_oas is not None and hy_oas >= HY_OAS_THRESHOLD:
        red_triggers.append(f"高收益信用利差 {hy_oas:.2f}% >= {HY_OAS_THRESHOLD}%")
    if net_liq_change is not None and net_liq_change <= NET_LIQUIDITY_DROP_THRESHOLD:
        red_triggers.append(f"净流动性3月变动 {net_liq_change:.1f}% <= {NET_LIQUIDITY_DROP_THRESHOLD}%")
    if vix_ratio is not None and vix_ratio > VIX_BACKWARDATION_THRESHOLD:
        red_triggers.append(f"VIX期货贴水 比值{vix_ratio:.2f} > {VIX_BACKWARDATION_THRESHOLD}")

    if red_triggers:
        state = "RED"
        state_reason = "触发条件: " + "; ".join(red_triggers)

    elif close < stop_level:
        state = "ORANGE"
        state_reason = f"QQQ {close:.2f} < 动态离场线 {stop_level:.2f} (SMA200 - 2.0*ATR14)"

    elif adx14 < ADX_MONKEY_THRESHOLD:
        state = "YELLOW"
        state_reason = f"ADX14 = {adx14:.1f} < {ADX_MONKEY_THRESHOLD}，市场无方向"

    else:
        state = "GREEN"
        state_reason = f"ADX14 = {adx14:.1f} >= {ADX_MONKEY_THRESHOLD} 且 QQQ {close:.2f} >= SMA200 {sma200:.2f}"

    report_date = latest_date.strftime("%Y-%m-%d")
    distance_pct = ((close - stop_level) / close) * 100

    state_map = {
        "RED": "🔴 RED - 黑天鹅/衰退紧急熔断",
        "ORANGE": "🟠 ORANGE - 技术面破位止损",
        "YELLOW": "🟡 YELLOW - 猴市震荡防磨损",
        "GREEN": "🟢 GREEN - 主升浪全速进攻",
    }
    action_map = {
        "RED": "100% SGOV 避险",
        "ORANGE": "100% SGOV 离场",
        "YELLOW": "100% QQQ (降杠杆避磨损)",
        "GREEN": "100% TQQQ 持有",
    }

    sahm_str = f"{sahm_value:.2f}%" if sahm_value is not None else "数据暂不可用"
    hy_str = f"{hy_oas * 100:.0f} 个基点" if hy_oas is not None else "数据暂不可用"
    t10y2y_str = f"{t10y2y:.2f}%" if t10y2y is not None else "数据暂不可用"
    liq_str = f"{'正' if net_liq_change >= 0 else '负'} {abs(net_liq_change):.1f}%" if net_liq_change is not None else "数据暂不可用"
    vix_str = f"{vix_ratio:.2f}，{'⚠️ 贴水(恐慌)' if vix_ratio > 1.0 else '升水正常，无机构恐慌'}" if vix_ratio is not None else "数据暂不可用"

    if adx14 >= 25:
        adx_comment = "强单边趋势"
    elif adx14 >= 20:
        adx_comment = "处于单边趋势"
    else:
        adx_comment = "无方向猴市"

    report = f"""📊【四维量化状态机报告】日期：{report_date}

当前推荐状态：{state_map[state]}
建议动作：{action_map[state]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
实时监控面板数据：

● QQQ 现价：${close:.2f} 美元
● 二百日均线：${sma200:.2f} 美元
● 十四日真实波幅：${atr14:.2f} 美元
● 动态离场线：${stop_level:.2f} 美元，当前价格{'高于' if distance_pct >= 0 else '低于'}离场线 {abs(distance_pct):.1f}%
● 趋势强度 ADX：{adx14:.1f}，{adx_comment}
● 萨姆规则数值：{sahm_str}，{'⚠️ 超过' if sahm_value is not None and sahm_value >= SAHM_THRESHOLD else '低于'} {SAHM_THRESHOLD}% 衰退线
● 高收益信用利差：{hy_str}，{'⚠️ 超过' if hy_oas is not None and hy_oas >= HY_OAS_THRESHOLD else '低于'} {HY_OAS_THRESHOLD * 100:.0f} 个基点警戒线
● VIX 期限结构比值：{vix_str}
● 美联储净流动性三个月变动：{liq_str}，{'⚠️ 资金面恶化' if net_liq_change is not None and net_liq_change <= NET_LIQUIDITY_DROP_THRESHOLD else '资金面健康'}
● 10Y-2Y 美债利差：{t10y2y_str}{"  ⚠️ 收益率曲线倒挂" if t10y2y is not None and t10y2y < 0 else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
决策依据：{state_reason}

操作建议：{"今日无需调仓，继续持有 TQQQ。" if state == "GREEN" else "⚡ 请立即调仓！" + action_map[state]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 State Machine v3.3 | Powered by yfinance + FRED + Aliyun VIX"""

    return report, state


# ============================================================
# 模块 B：QDII 基金公告监控
# ============================================================
def load_qdii_history() -> list | None:
    """从 S3 读取 QDII 公告推送历史"""
    if not s3_client or not S3_BUCKET:
        return []
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_STATE_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))
    except Exception as e:
        logger.warning(f"[QDII] 读取历史记录提示: {e}")
        return []


def save_qdii_history(history: list):
    """将 QDII 公告历史保存到 S3"""
    if not s3_client or not S3_BUCKET:
        return
    try:
        if len(history) > 500:
            history = history[-500:]
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=S3_STATE_KEY,
            Body=json.dumps(history, ensure_ascii=False, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as e:
        logger.error(f"[QDII] S3 保存历史记录失败: {e}")


def run_qdii_monitor():
    """执行 QDII 基金公告监控（仅景顺长城全球半导体芯片）"""
    logger.info(f"[QDII] 开始扫描基金公告 (过滤 {CUTOFF_DATE_STR} 之前的数据)...")

    history = load_qdii_history() or []

    headers = {
        "Authorization": f"APPCODE {ALIYUN_APPCODE}",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    new_notices_found = []

    for fund_code, fund_name in QDII_FUNDS.items():
        logger.info(f"[QDII] 正在查询: {fund_name} ({fund_code})")
        payload = {"fundCode": fund_code, "pageNo": "1", "pageSize": "10"}

        try:
            response = requests.post(QDII_API_URL, headers=headers, data=payload, timeout=10)
            if response.status_code != 200:
                logger.error(f"[QDII] 接口 HTTP 错误，状态码: {response.status_code}")
                continue

            try:
                result = response.json()
            except ValueError:
                logger.error(f"[QDII] 数据解析失败，接口返回非法内容")
                continue

            notices = result.get("data", {}).get("list", [])
            if not notices:
                continue

            for notice in notices:
                title = notice.get("title")
                date_str = notice.get("date")

                if not title or not date_str:
                    continue

                title = str(title)
                date_str = str(date_str)

                if date_str < CUTOFF_DATE_STR:
                    continue
                if "提示性公告" in title:
                    continue

                unique_id = f"{fund_code}_{date_str}_{title}"
                if unique_id in history:
                    continue

                is_trigger = False
                emoji = "📢"

                if "定期定额" in title:
                    is_trigger = True
                    emoji = "💴"
                elif "季度报告" in title or "年度报告" in title:
                    is_trigger = True
                    emoji = "📄"
                elif "非交易日" in title or "节假日" in title:
                    is_trigger = True
                    emoji = "☀️"

                if is_trigger:
                    new_notices_found.append({
                        "fund_name": fund_name,
                        "title": title,
                        "date": date_str,
                        "emoji": emoji,
                        "unique_id": unique_id,
                    })

        except Exception as e:
            logger.error(f"[QDII] 查询 {fund_code} 时发生错误: {e}")

    if new_notices_found:
        success_count = 0
        for notice in new_notices_found:
            msg_title = f"{notice['emoji']} {notice['fund_name']}"
            msg_body = f"{notice['title']}\n发布日期：{notice['date']}"
            if send_bark(msg_title, msg_body, "基金监控"):
                history.append(notice["unique_id"])
                success_count += 1
        save_qdii_history(history)
        logger.info(f"[QDII] 发现 {len(new_notices_found)} 条公告，成功推送 {success_count} 条")
    else:
        logger.info("[QDII] 平安无事，没有发现符合条件的公告")

    return f"QDII 监控完毕，推送 {len(new_notices_found)} 条"


# ============================================================
# 入口函数（兼容 AWS Lambda 与 Docker/本地命令行直跑）
# ============================================================
def lambda_handler(event=None, context=None):
    """
    AWS Lambda / 容器标准入口
    """
    logger.info("====== 统一监控系统 v3.3 启动 ======")
    results = {}

    # ---- 模块 A：四维量化状态机 ----
    try:
        report, state = run_state_machine()

        if state == "GREEN":
            logger.info("[状态机] GREEN 绿色静默模式，不发送 Bark 推送。")
            logger.info(f"[状态机] 报告内容:\n{report}")
            results["state_machine"] = "GREEN_silent"
        elif state == "YELLOW":
            send_bark("⚠️ [YELLOW] 市场进入猴市震荡", report, "量化监控")
            results["state_machine"] = "YELLOW_notified"
        elif state == "ORANGE":
            send_bark("⚠️ [ORANGE] 技术线破位止损", report, "量化监控")
            results["state_machine"] = "ORANGE_notified"
        elif state == "RED":
            send_bark("⚠️ [RED ALERT] 黑天鹅/衰退紧急熔断", report, "量化监控")
            results["state_machine"] = "RED_notified"

    except Exception as e:
        error_msg = f"⚠️ 状态机监控异常\n\n错误类型: {type(e).__name__}\n错误详情: {str(e)}"
        logger.error(f"[状态机] 运行异常: {e}", exc_info=True)
        send_bark("⚠️ 状态机监控异常", error_msg, "量化监控")
        results["state_machine"] = f"error: {e}"

    # ---- 模块 B：QDII 基金公告 ----
    try:
        qdii_result = run_qdii_monitor()
        results["qdii"] = qdii_result
    except Exception as e:
        error_msg = f"⚠️ QDII 监控异常\n\n错误类型: {type(e).__name__}\n错误详情: {str(e)}"
        logger.error(f"[QDII] 运行异常: {e}", exc_info=True)
        send_bark("⚠️ QDII 监控异常", error_msg, "基金监控")
        results["qdii"] = f"error: {e}"

    logger.info(f"====== 监控完毕: {results} ======")
    return {
        "statusCode": 200,
        "body": json.dumps(results, ensure_ascii=False)
    }


if __name__ == "__main__":
    print(lambda_handler())